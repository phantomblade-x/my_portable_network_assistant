"""
Main assistant logic - ties everything together
"""

import json
import re
from typing import Optional, Dict, Any
from pathlib import Path

from cisco.commands import ALL_COMMANDS, READ_COMMANDS, EXEC_COMMANDS, PrivilegeLevel
from confirmation import VoiceConfirmation


class NetworkAssistant:
    def __init__(self, llm, cisco, stt, tts, exec_password: str, wake_word: str = "hey cisco"):
        self.llm = llm
        self.cisco = cisco
        self.stt = stt
        self.tts = tts
        self.wake_word = wake_word.lower()
        self.confirm = VoiceConfirmation(exec_password, stt, tts)
        
        # Load prompts
        self.intent_prompt = self._load_prompt('intent_extraction.txt')
        self.interpret_prompt = self._load_prompt('output_interpretation.txt')
    
    def _load_prompt(self, filename: str) -> str:
        path = Path(__file__).parent.parent / 'prompts' / filename
        if path.exists():
            return path.read_text()
        return ""
    
    def run(self):
        """Main listening loop"""
        while True:
            # Listen for wake word
            audio = self.stt.listen(timeout=None)  # Listen indefinitely
            
            if audio and self.wake_word in audio.lower():
                # Remove wake word from query
                query = re.sub(
                    re.escape(self.wake_word), 
                    '', 
                    audio, 
                    flags=re.IGNORECASE
                ).strip()
                
                if query:
                    self.handle_query(query)
                else:
                    # Just wake word, prompt for command
                    self.tts.speak("Yes?")
                    query = self.stt.listen(timeout=10)
                    if query:
                        self.handle_query(query)
    
    def handle_query(self, spoken_text: str):
        """Process a voice query"""
        
        # Parse intent using LLM
        intent = self.parse_intent(spoken_text)
        
        if not intent or intent.get('action') not in ALL_COMMANDS:
            self.tts.speak("Sorry, I don't know how to do that. Try asking about VLANs, port status, or MAC addresses.")
            return
        
        action = intent['action']
        cmd_def = ALL_COMMANDS[action]
        
        # Build description with actual values
        try:
            description = cmd_def.description.format(**intent)
        except KeyError:
            description = cmd_def.description
        
        # Check if exec mode required
        if cmd_def.privilege == PrivilegeLevel.EXEC:
            if not self.confirm.request_confirmation(description):
                return
            self.cisco.enter_config_mode()
        
        # Build and execute command
        try:
            command = cmd_def.template.format(**intent)
        except KeyError as e:
            self.tts.speak(f"I'm missing some information: {e}")
            return
        
        output = self.cisco.send_command(command)
        
        # Exit config mode if needed
        if cmd_def.privilege == PrivilegeLevel.EXEC:
            self.cisco.exit_config_mode()
        
        # Interpret output
        response = self.interpret_output(spoken_text, output)
        self.tts.speak(response)
    
    def parse_intent(self, text: str) -> Optional[Dict[str, Any]]:
        """Use LLM to extract intent from natural language"""
        
        actions_list = ', '.join(ALL_COMMANDS.keys())
        
        prompt = f"""Extract the intent from this network query. Return JSON only.

Query: "{text}"

Valid actions: {actions_list}

For interface names, convert spoken words to Cisco format:
- "port 5" or "port five" → "Gi1/0/5"
- "gigabit 1/0/5" → "Gi1/0/5"
- "blade 4 port 16" → "Gi4/0/16" (assume blade maps to port numbering)

Examples:
- "what vlan is port 16 on" → {{"action": "get_vlan", "interface": "Gi1/0/16"}}
- "shut down port 24" → {{"action": "shutdown_port", "interface": "Gi1/0/24"}}
- "put port 12 on vlan 100" → {{"action": "set_vlan", "interface": "Gi1/0/12", "vlan": "100"}}
- "show me the vlans" → {{"action": "show_vlans"}}
- "any errors on port 8" → {{"action": "show_errors", "interface": "Gi1/0/8"}}

Return only valid JSON:"""

        try:
            result = self.llm.complete(prompt, max_tokens=150, temperature=0.1)
            # Extract JSON from response
            json_match = re.search(r'\{[^}]+\}', result)
            if json_match:
                return json.loads(json_match.group())
        except (json.JSONDecodeError, Exception) as e:
            print(f"Intent parsing error: {e}")
        
        return None
    
    def interpret_output(self, question: str, output: str) -> str:
        """Use LLM to create human-friendly response"""
        
        prompt = f"""You are a helpful network assistant. Answer the user's question based on this Cisco switch output.
Be concise - this will be spoken aloud. One or two sentences max.

User's question: {question}

Switch output:
{output}

Response:"""

        try:
            return self.llm.complete(prompt, max_tokens=100, temperature=0.3)
        except Exception as e:
            return f"I got a response from the switch but had trouble interpreting it."
