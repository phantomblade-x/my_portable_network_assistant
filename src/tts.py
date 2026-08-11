"""
Text-to-Speech using Piper
"""

import subprocess
import tempfile
import sounddevice as sd
import numpy as np
from pathlib import Path


class PiperTTS:
    def __init__(self, model_path: str, config_path: str, sample_rate: int = 22050):
        self.model_path = model_path
        self.config_path = config_path
        self.sample_rate = sample_rate
    
    def speak(self, text: str):
        """Convert text to speech and play it"""
        print(f"🔊 Speaking: {text}")
        
        # Use piper CLI to generate audio
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            temp_path = f.name
        
        try:
            subprocess.run([
                'piper',
                '--model', self.model_path,
                '--config', self.config_path,
                '--output_file', temp_path
            ], input=text.encode(), check=True, capture_output=True)
            
            # Play the audio
            import wave
            with wave.open(temp_path, 'rb') as wf:
                audio = np.frombuffer(
                    wf.readframes(wf.getnframes()),
                    dtype=np.int16
                ).astype(np.float32) / 32768.0
                
                sd.play(audio, wf.getframerate())
                sd.wait()
        
        finally:
            Path(temp_path).unlink(missing_ok=True)