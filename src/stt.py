"""
Speech-to-Text using Whisper.cpp
"""

import numpy as np
import sounddevice as sd
from whispercpp import Whisper
from typing import Optional


class WhisperSTT:
    def __init__(self, model_path: str, sample_rate: int = 16000):
        self.whisper = Whisper.from_pretrained(model_path)
        self.sample_rate = sample_rate
    
    def listen(self, timeout: Optional[float] = 10, silence_threshold: float = 0.01) -> Optional[str]:
        """
        Record audio and transcribe it.
        
        Args:
            timeout: Max seconds to record (None for indefinite until silence)
            silence_threshold: RMS threshold to detect silence
        
        Returns:
            Transcribed text or None if nothing detected
        """
        print("🎤 Listening...")
        
        # Record audio
        duration = timeout or 30  # Max 30 seconds if no timeout
        audio = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype=np.float32
        )
        sd.wait()
        
        # Trim silence from end
        audio = audio.flatten()
        audio = np.trim_zeros(audio, 'b')
        
        if len(audio) < self.sample_rate * 0.5:  # Less than 0.5s of audio
            return None
        
        # Transcribe
        result = self.whisper.transcribe(audio)
        text = result.strip()
        
        if text:
            print(f"📝 Heard: {text}")
        
        return text if text else None