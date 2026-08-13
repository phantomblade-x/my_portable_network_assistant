#!/usr/bin/env python3
"""
Cisco Voice Assistant - Main entry point
"""

import yaml
import signal
import sys
from pathlib import Path

from assistant import NetworkAssistant
from stt import WhisperSTT
from tts import PiperTTS
from llm import LocalLLM
from cisco.console import CiscoConsole


def load_config(path: str = "config.yaml") -> dict:
    with open(path, 'r') as f:
        return yaml.safe_load(f)


def main():
    print("🔌 Cisco Voice Assistant starting...")
    
    # Load config
    config = load_config()
    
    # Initialize components
print("  Loading Whisper STT...")
stt = WhisperSTT(
    config['models']['whisper'],
    sample_rate=config['audio']['sample_rate'],
    mic_device=config['audio'].get('mic_device')
)
    
    print("  Loading Piper TTS...")
    tts = PiperTTS(
        config['models']['piper_model'],
        config['models']['piper_config']
    )
    
    print("  Loading LLM...")
    llm = LocalLLM(
        config['models']['llm'],
        context_length=config['llm']['context_length'],
        threads=config['llm']['threads']
    )
    
    print("  Connecting to serial console...")
    cisco = CiscoConsole(
        port=config['serial']['port'],
        baud=config['serial']['baud']
    )
    
    # Create assistant
    assistant = NetworkAssistant(
        llm=llm,
        cisco=cisco,
        stt=stt,
        tts=tts,
        exec_password=config['exec_password'],
        wake_word=config.get('wake_word', 'hey cisco')
    )
    
    # Handle graceful shutdown
    def signal_handler(sig, frame):
        print("\n👋 Shutting down...")
        cisco.close()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start listening
    print("✅ Ready! Say '{}' to begin.".format(config.get('wake_word', 'hey cisco')))
    tts.speak("Cisco voice assistant ready.")
    
    assistant.run()


if __name__ == "__main__":
    main()
