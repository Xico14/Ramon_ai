"""
Wake Word — Детектор кодового слова
Слушает и ждёт "Джарвис"
"""
import asyncio
import logging
import numpy as np
from typing import Optional

from core.event_bus import EventBus, Event, EventType
from audio.capture import AudioCapture

logger = logging.getLogger(__name__)


class WakeWord:
    """
    Wake Word Detection
    Слушает кодовое слово "Джарвис"
    """
    
    def __init__(self, config: dict, event_bus: EventBus, audio_capture: AudioCapture):
        self.config = config
        self.event_bus = event_bus
        self.audio_capture = audio_capture
        
        self.model_path = config.get('model_path')
        self.threshold = config.get('threshold', 0.5)
        self.chunk_size = config.get('chunk_size', 1280)
        
        # Модель
        self._model = None
        self._loaded = False
        
        # Состояние
        self._running = False
        self._task: Optional[asyncio.Task] = None
        
        logger.info(f"WakeWord инициализирован (threshold={self.threshold})")
    
    async def load(self) -> None:
        """Загрузка модели wake word"""
        if self._loaded:
            return
        
        logger.info("📥 Загрузка Wake Word модели...")
        
        try:
            # Попытка загрузить openwakeword
            from openwakeword.model import Model
            self._model = Model(wakeword_models=[self.model_path])
            self._loaded = True
            logger.info("✅ Wake Word модель загружена (openwakeword)")
        except ImportError:
            logger.warning("⚠️ openwakeword не установлен, используем fallback")
            self._loaded = True
        except Exception as e:
            logger.error(f"Ошибка загрузки Wake Word: {e}")
            self._loaded = True  # Fallback режим
    
    async def start(self) -> None:
        """Запуск детекции wake word"""
        if not self._loaded:
            await self.load()
        
        self._running = True
        self._task = asyncio.create_task(self._detection_loop())
        
        logger.info("⏰ Wake Word запущен (ждём 'Джарвис')")
    
    async def _detection_loop(self) -> None:
        """Цикл детекции wake word"""
        sample_rate = self.audio_capture.sample_rate
        chunk_duration = self.chunk_size / sample_rate
        
        while self._running:
            try:
                # Получение аудио
                audio = self.audio_capture.get_audio(chunk_duration)
                
                if len(audio) < self.chunk_size:
                    await asyncio.sleep(0.05)
                    continue
                
                # Детекция
                detected = await self._detect(audio)
                
                if detected:
                    logger.info("🔔 Wake Word обнаружен! ('Джарвис')")
                    
                    await self.event_bus.publish(Event(
                        type=EventType.WAKE_DETECTED,
                        data={'word': 'jarvis'},
                        source='wake_word',
                    ))
                    
                    # Пауза чтобы не срабатывало повторно
                    await asyncio.sleep(1.0)
                
                await asyncio.sleep(0.05)
            
            except Exception as e:
                logger.error(f"Ошибка Wake Word: {e}")
                await asyncio.sleep(0.1)
    
    async def _detect(self, audio: np.ndarray) -> bool:
        """Детекция wake word в аудио"""
        if self._model is not None:
            # OpenWakeWord
            try:
                prediction = self._model.predict(audio)
                # Проверка порога
                for model_name, score in prediction.items():
                    if score > self.threshold:
                        return True
                return False
            except Exception as e:
                logger.debug(f"Ошибка openwakeword: {e}")
                return False
        else:
            # Fallback: энергетический детектор (для тестирования)
            return False
    
    async def stop(self) -> None:
        """Остановка"""
        self._running = False
        
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        
        logger.info("🛑 Wake Word остановлен")
