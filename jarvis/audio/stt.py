"""
STT — Speech-to-Text (Распознавание речи)
faster-whisper для преобразования звука в текст
"""
import asyncio
import logging
import numpy as np
from typing import Optional

from core.event_bus import EventBus, Event, EventType
from audio.capture import AudioCapture

logger = logging.getLogger(__name__)


class STT:
    """
    Speech-to-Text
    Использует faster-whisper для распознавания речи
    """
    
    def __init__(self, config: dict, event_bus: EventBus, audio_capture: AudioCapture):
        self.config = config
        self.event_bus = event_bus
        self.audio_capture = audio_capture
        
        self.model_size = config.get('model_size', 'large-v3')
        self.language = config.get('language', 'ru')
        self.device = config.get('device', 'cpu')
        self.compute_type = config.get('compute_type', 'int8')
        self.beam_size = config.get('beam_size', 5)
        
        # Whisper модель
        self._model = None
        self._loaded = False
        
        # Состояние
        self._listening = False
        
        logger.info(f"STT инициализирован (model={self.model_size}, lang={self.language})")
    
    async def load(self) -> None:
        """Загрузка модели faster-whisper"""
        if self._loaded:
            return
        
        logger.info(f"📥 Загрузка Whisper модели ({self.model_size})...")
        
        try:
            from faster_whisper import WhisperModel
            
            loop = asyncio.get_event_loop()
            self._model = await loop.run_in_executor(
                None,
                lambda: WhisperModel(
                    self.model_size,
                    device=self.device,
                    compute_type=self.compute_type,
                )
            )
            
            self._loaded = True
            logger.info("✅ Whisper модель загружена")
        
        except Exception as e:
            logger.error(f"Ошибка загрузки Whisper: {e}")
            raise
    
    async def start_listening(self) -> None:
        """Начать слушать (подписка на события)"""
        if not self._loaded:
            await self.load()
        
        self._listening = True
        self.event_bus.subscribe(EventType.SPEECH_ENDED, self._on_speech_ended)
        
        logger.info("👂 STT начал слушать")
    
    async def stop_listening(self) -> None:
        """Перестать слушать"""
        self._listening = False
        self.event_bus.unsubscribe(EventType.SPEECH_ENDED, self._on_speech_ended)
        
        logger.info("🔇 STT перестал слушать")
    
    async def _on_speech_ended(self, event: Event) -> None:
        """Обработка окончания речи"""
        if not self._listening:
            return
        
        # Получение аудио за время речи
        start_time = event.data.get('start_time')
        end_time = event.data.get('end_time')
        duration = end_time - start_time
        
        # Добавляем padding
        padding = 0.1  # 100 ms
        audio = self.audio_capture.get_audio(duration + padding * 2)
        
        if len(audio) == 0:
            logger.warning("Пустое аудио для распознавания")
            return
        
        # Распознавание
        text = await self.transcribe(audio)
        
        if text:
            await self.event_bus.publish(Event(
                type=EventType.TEXT_TRANSCRIBED,
                data={'text': text},
                source='stt',
            ))
    
    async def transcribe(self, audio: np.ndarray) -> str:
        """
        Распознавание речи
        Возвращает текст
        """
        if not self._loaded:
            await self.load()
        
        logger.debug(f"Распознавание аудио ({len(audio)} сэмплов)...")
        
        try:
            loop = asyncio.get_event_loop()
            
            # Транскрибация в отдельном потоке
            segments, info = await loop.run_in_executor(
                None,
                lambda: self._model.transcribe(
                    audio,
                    language=self.language,
                    beam_size=self.beam_size,
                    vad_filter=True,
                )
            )
            
            # Сборка текста из сегментов
            text_parts = []
            for segment in segments:
                text_parts.append(segment.text)
            
            text = ''.join(text_parts).strip()
            
            logger.info(f"📝 Распознано: {text}")
            
            return text
        
        except Exception as e:
            logger.error(f"Ошибка распознавания: {e}")
            return ""
    
    async def stop(self) -> None:
        """Остановка STT"""
        await self.stop_listening()
        self._model = None
        self._loaded = False
        
        logger.info("🛑 STT остановлен")
    
    @property
    def is_loaded(self) -> bool:
        """Загружена ли модель"""
        return self._loaded
