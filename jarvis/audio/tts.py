"""
TTS — Text-to-Speech (Синтез речи)
Streaming TTS для озвучивания ответов
"""
import asyncio
import logging
import numpy as np
from typing import Optional
from pathlib import Path

from core.event_bus import EventBus, Event, EventType

logger = logging.getLogger(__name__)


class TTS:
    """
    Text-to-Speech
    Streaming синтез речи
    """
    
    def __init__(self, config: dict, event_bus: EventBus):
        self.config = config
        self.event_bus = event_bus
        
        self.model_path = config.get('model_path')
        self.speaker = config.get('speaker', 'default')
        self.speed = config.get('speed', 1.0)
        self.sample_rate = config.get('sample_rate', 24000)
        
        # TTS модель
        self._model = None
        self._loaded = False
        
        # Состояние
        self._speaking = False
        self._stop_requested = False
        
        # Audio playback
        self._pa = None
        self._stream = None
        
        logger.info(f"TTS инициализирован (sample_rate={self.sample_rate})")
    
    async def load(self) -> None:
        """Загрузка TTS модели"""
        if self._loaded:
            return
        
        if self.model_path and Path(self.model_path).exists():
            logger.info(f"📥 Загрузка TTS модели из {self.model_path}...")
            # TODO: Загрузка реальной TTS модели
            # Например: Coqui TTS, Silero TTS, или другая
            self._loaded = True
            logger.info("✅ TTS модель загружена")
        else:
            logger.warning("⚠️ TTS модель не найдена, используется fallback")
            self._loaded = True
    
    async def speak(self, text: str) -> None:
        """
        Озвучить текст
        Streaming — начинает говорить с первого слова
        """
        if not self._loaded:
            await self.load()
        
        self._speaking = True
        self._stop_requested = False
        
        await self.event_bus.publish(Event(
            type=EventType.TTS_GENERATING,
            data={'text': text},
            source='tts',
        ))
        
        try:
            # Разбиение текста на предложения для streaming
            sentences = self._split_into_sentences(text)
            
            for sentence in sentences:
                if self._stop_requested:
                    break
                
                # Генерация аудио для предложения
                audio = await self._generate_audio(sentence)
                
                if audio is not None and len(audio) > 0:
                    # Воспроизведение
                    await self._play_audio(audio)
            
            if not self._stop_requested:
                await self.event_bus.publish(Event(
                    type=EventType.TTS_COMPLETED,
                    data={'text': text},
                    source='tts',
                ))
        
        except Exception as e:
            logger.error(f"Ошибка TTS: {e}")
        
        finally:
            self._speaking = False
    
    def _split_into_sentences(self, text: str) -> list[str]:
        """Разбиение текста на предложения"""
        import re
        # Разбиение по точкам, вопросительным и восклицательным знакам
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    async def _generate_audio(self, text: str) -> Optional[np.ndarray]:
        """Генерация аудио для текста"""
        # TODO: Реальная генерация с помощью TTS модели
        # Пока используем заглушку
        
        logger.debug(f"Генерация аудио для: {text[:50]}...")
        
        # Заглушка: тишина
        duration = len(text) * 0.05  # Примерно 50 ms на символ
        samples = int(self.sample_rate * duration)
        audio = np.zeros(samples, dtype=np.float32)
        
        return audio
    
    async def _play_audio(self, audio: np.ndarray) -> None:
        """Воспроизведение аудио"""
        try:
            import pyaudio
            
            if self._pa is None:
                self._pa = pyaudio.PyAudio()
            
            if self._stream is None:
                self._stream = self._pa.open(
                    format=pyaudio.paFloat32,
                    channels=1,
                    rate=self.sample_rate,
                    output=True,
                )
            
            await self.event_bus.publish(Event(
                type=EventType.TTS_SPEAKING,
                data={'samples': len(audio)},
                source='tts',
            ))
            
            # Воспроизведение в отдельном потоке
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                lambda: self._stream.write(audio.astype(np.float32).tobytes())
            )
        
        except Exception as e:
            logger.error(f"Ошибка воспроизведения: {e}")
    
    async def stop_speaking(self) -> None:
        """Остановить воспроизведение (barge-in)"""
        self._stop_requested = True
        self._speaking = False
        
        if self._stream:
            self._stream.stop_stream()
        
        await self.event_bus.publish(Event(
            type=EventType.AUDIO_PLAYBACK_STOPPED,
            data={'reason': 'barge_in'},
            source='tts',
        ))
        
        logger.info("🛑 TTS остановлен (barge-in)")
    
    async def stop(self) -> None:
        """Полная остановка TTS"""
        await self.stop_speaking()
        
        if self._stream:
            self._stream.close()
        
        if self._pa:
            self._pa.terminate()
        
        self._model = None
        self._loaded = False
        
        logger.info("🛑 TTS остановлен")
    
    @property
    def is_speaking(self) -> bool:
        """Воспроизводится ли речь сейчас"""
        return self._speaking
