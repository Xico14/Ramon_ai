"""
VAD — Voice Activity Detection (Детектор речи)
Silero v5 — определяет, когда человек говорит
"""
import asyncio
import logging
import numpy as np
from typing import Optional, Callable

from core.event_bus import EventBus, Event, EventType
from audio.capture import AudioCapture

logger = logging.getLogger(__name__)


class VAD:
    """
    Voice Activity Detection
    Определяет начало и конец речи
    """
    
    def __init__(self, config: dict, event_bus: EventBus, audio_capture: AudioCapture):
        self.config = config
        self.event_bus = event_bus
        self.audio_capture = audio_capture
        
        self.threshold = config.get('threshold', 0.5)
        self.min_speech_ms = config.get('min_speech_ms', 250)
        self.min_silence_ms = config.get('min_silence_ms', 500)
        self.padding_ms = config.get('padding_ms', 100)
        
        # Silero VAD модель
        self._model = None
        self._loaded = False
        
        # Состояние
        self._is_speaking = False
        self._speech_start_time: Optional[float] = None
        self._silence_start_time: Optional[float] = None
        
        # Задача
        self._running = False
        self._task: Optional[asyncio.Task] = None
        
        logger.info(f"VAD инициализирован (threshold={self.threshold})")
    
    async def load(self) -> None:
        """Загрузка модели Silero VAD"""
        if self._loaded:
            return
        
        logger.info("📥 Загрузка Silero VAD...")
        
        try:
            import torch
            self._model, utils = torch.hub.load(
                repo_or_dir='snakers4/silero-vad',
                model='silero_vad',
                force_reload=False,
            )
            self._get_speech_timestamps, _, _, _, _ = utils
            self._loaded = True
            logger.info("✅ Silero VAD загружен")
        except Exception as e:
            logger.error(f"Ошибка загрузки Silero VAD: {e}")
            # Fallback: используем простой энергетический детектор
            self._model = None
            self._loaded = True
            logger.warning("⚠️ Используем fallback VAD (энергетический)")
    
    async def start(self) -> None:
        """Запуск VAD"""
        if not self._loaded:
            await self.load()
        
        self._running = True
        self._task = asyncio.create_task(self._vad_loop())
        
        logger.info("👂 VAD запущен")
    
    async def _vad_loop(self) -> None:
        """Цикл обработки VAD"""
        sample_rate = self.audio_capture.sample_rate
        chunk_duration = 0.03  # 30 ms chunks для VAD
        chunk_samples = int(sample_rate * chunk_duration)
        
        while self._running:
            try:
                # Получение последних 30 ms аудио
                audio_chunk = self.audio_capture.get_audio(chunk_duration)
                
                if len(audio_chunk) < chunk_samples:
                    await asyncio.sleep(0.01)
                    continue
                
                # Определение речи
                is_speech = await self._detect_speech(audio_chunk, sample_rate)
                
                current_time = asyncio.get_event_loop().time()
                
                # Обработка состояния
                if is_speech and not self._is_speaking:
                    # Начало речи
                    self._is_speaking = True
                    self._speech_start_time = current_time
                    self._silence_start_time = None
                    
                    await self.event_bus.publish(Event(
                        type=EventType.SPEECH_DETECTED,
                        data={'timestamp': current_time},
                        source='vad',
                    ))
                    logger.debug("🗣️ Речь обнаружена")
                
                elif is_speech and self._is_speaking:
                    # Продолжение речи
                    self._silence_start_time = None
                
                elif not is_speech and self._is_speaking:
                    # Тишина во время речи
                    if self._silence_start_time is None:
                        self._silence_start_time = current_time
                    else:
                        silence_duration = (current_time - self._silence_start_time) * 1000  # ms
                        if silence_duration >= self.min_silence_ms:
                            # Конец речи
                            speech_duration = (current_time - self._speech_start_time) * 1000  # ms
                            
                            if speech_duration >= self.min_speech_ms:
                                await self.event_bus.publish(Event(
                                    type=EventType.SPEECH_ENDED,
                                    data={
                                        'duration_ms': speech_duration,
                                        'start_time': self._speech_start_time,
                                        'end_time': current_time,
                                    },
                                    source='vad',
                                ))
                                logger.debug(f"🔇 Речь закончилась ({speech_duration:.0f} ms)")
                            
                            self._is_speaking = False
                            self._speech_start_time = None
                            self._silence_start_time = None
                
                await asyncio.sleep(0.01)  # 10 ms pause
            
            except Exception as e:
                logger.error(f"Ошибка VAD: {e}")
                await asyncio.sleep(0.1)
    
    async def _detect_speech(self, audio: np.ndarray, sample_rate: int) -> bool:
        """Определение речи в аудио чанке"""
        if self._model is not None:
            # Silero VAD
            try:
                import torch
                audio_tensor = torch.FloatTensor(audio)
                confidence = self._model(audio_tensor, sample_rate).item()
                return confidence > self.threshold
            except Exception as e:
                logger.debug(f"Ошибка Silero VAD: {e}")
                return self._fallback_detect(audio)
        else:
            # Fallback: энергетический детектор
            return self._fallback_detect(audio)
    
    def _fallback_detect(self, audio: np.ndarray) -> bool:
        """Простой энергетический детектор (fallback)"""
        energy = np.mean(audio ** 2)
        threshold = 0.01  # Настраиваемый порог энергии
        return energy > threshold
    
    async def stop(self) -> None:
        """Остановка VAD"""
        self._running = False
        
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        
        logger.info("🛑 VAD остановлен")
    
    @property
    def is_speaking(self) -> bool:
        """Обнаруживается ли речь сейчас"""
        return self._is_speaking
