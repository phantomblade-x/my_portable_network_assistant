"""
Voice-based password confirmation for exec commands
"""

import hashlib
from typing import Optional


class VoiceConfirmation:
    def __init__(self, password_phrase: str, stt, tts, timeout: int = 10):
        self.password_hash = self._hash(password_phrase)
        self.stt = stt
        self.tts = tts
        self.timeout = timeout
    
    def _hash(self, text: str) -> str:
        normalized = text.lower().strip()
        return hashlib.sha256(normalized.encode()).hexdigest()
    
    def _normalize(self, text: str) -> str:
        # Handle common phonetic variations
        replacements = {
            'alfa': 'alpha',
            'niner': 'nine',
            'fiver': 'five',
        }
        text = text.lower().strip()
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text
    
    def verify(self, spoken: str) -> bool:
        spoken_hash = self._hash(self._normalize(spoken))
        return spoken_hash == self.password_hash
    
    def request_confirmation(self, action_description: str) -> bool:
        """
        Request spoken password confirmation.
        Returns True if confirmed, False otherwise.
        """
        # Announce what we're about to do
        self.tts.speak(
            f"I'm about to {action_description}. "
            f"Please say the password to confirm, or say cancel."
        )
        
        # Listen for response
        spoken = self.stt.listen(timeout=self.timeout)
        
        if not spoken:
            self.tts.speak("I didn't hear anything. Command cancelled.")
            return False
        
        if 'cancel' in spoken.lower() or 'abort' in spoken.lower():
            self.tts.speak("Command cancelled.")
            return False
        
        if self.verify(spoken):
            self.tts.speak("Confirmed. Executing now.")
            return True
        else:
            self.tts.speak("Incorrect password. Command cancelled.")
            return False