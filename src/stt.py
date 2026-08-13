"""
Speech-to-Text using pywhispercpp
"""

import numpy as np
import sounddevice as sd
from pywhispercpp.model import Model
from typing import Optional


class WhisperSTT:
    def __init__(self, model_name: str, sample_rate: int = 16000):
        # model_name can be: tiny.en, base.en, small.en, etc.
        # pywhispercpp auto-downloads and caches
        self.whisper = Model(model_name, n_threads=4)
        self.sample_rate = sample_rate
    
    def listen(self, timeout: Optional[float] = 10, silence_threshold: float = 0.01) -> Optional[str]:
        """
        Record audio and transcribe it.
        """
        print("🎤 Listening...")
        
        duration = timeout or 30
        audio = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype=np.float32
        )
        sd.wait()
        
        audio = audio.flatten()
        
        if len(audio) < self.sample_rate * 0.5:
            return None
        
        # pywhispercpp transcribe returns a list of segments
        segments = self.whisper.transcribe(audio)
        text = " ".join([seg.text for seg in segments]).strip()
        
        if text:
            print(f"📝 Heard: {text}")
        
        return text if text else None
