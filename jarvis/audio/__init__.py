"""Audio package — Аудио подсистема"""
from audio.capture import AudioCapture
from audio.vad import VAD
from audio.stt import STT
from audio.tts import TTS

__all__ = ['AudioCapture', 'VAD', 'STT', 'TTS']
