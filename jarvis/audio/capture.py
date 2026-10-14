"""
Audio Capture — Захват звука с микрофона
16 kHz в кольцевой буфер
"""
import asyncio
import logging
import numpy as np
from collections import deque
from typing import Optional

from core.event_bus import EventBus, Event, EventType

logger = logging.getLogger(__name__)


class RingBuffer:
    """Кольцевой буфер для аудио данных"""
    
    def __init__(self, max_size: int):
        self._buffer: deque = deque(maxlen=max_size)
        self._max_size = max_size
    
    def append(self, data: np.ndarray) -> None:
        """Добавить данные в буфер"""
        self._buffer.append(data)
    
    def get_all(self) -> np.ndarray:
        """Получить все данные"""
        if not self._buffer:
            return np.array([], dtype=np.float32)
        return np.concatenate(list(self._buffer))
    
    def clear(self) -> None:
        """Очистить буфер"""
        self._buffer.clear()
    
    @property
    def size(self) -> int:
        """Размер буфера в сэмплах"""
        return sum(len(chunk) for chunk in self._buffer)


class AudioCapture:
    """
    Захват звука с микрофона
    16 kHz, mono, 16-bit PCM
    """
    
    def __init__(self, config: dict, event_bus: EventBus):
        self.config = config
        self.event_bus = event_bus
        
        self.sample_rate = config.get('sample_rate_input', 16000)
        self.channels = config.get('channels', 1)
        self.chunk_size = config.get('chunk_size', 512)
        self.buffer_seconds = config.get('ring_buffer_seconds', 2.0)
        
        # Кольцевой буфер
        buffer_size = int(self.sample_rate * self.buffer_seconds)
        self.ring_buffer = RingBuffer(buffer_size)
        
        # PyAudio
        self._pa = None
        self._stream = None
        self._running = False
        self._task: Optional[asyncio.Task] = None
        
        logger.info(f"AudioCapture инициализирован ({self.sample_rate} Hz, {self.chunk_size} samples)")
    
    async def start(self) -> None:
        """Запуск захвата звука"""
        if self._running:
            return
        
        try:
            import pyaudio
        except ImportError:
            logger.error("PyAudio не установлен. Запустите: pip install pyaudio")
            return
        
        self._pa = pyaudio.PyAudio()
        
        # Открытие потока
        self._stream = self._pa.open(
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
        )
        
        self._running = True
        self._task = asyncio.create_task(self._capture_loop())
        
        logger.info("🎤 AudioCapture запущен")
    
    async def _capture_loop(self) -> None:
        """Цикл захвата звука"""
        while self._running:
            try:
                # Чтение данных (в отдельном потоке)
                loop = asyncio.get_event_loop()
                data = await loop.run_in_executor(None, self._read_chunk)
                
                if data is not None:
                    # Конвертация в numpy array
                    audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
                    
                    # Добавление в кольцевой буфер
                    self.ring_buffer.append(audio_data)
                    
                    # Публикация события
                    await self.event_bus.publish(Event(
                        type=EventType.AUDIO_CAPTURED,
                        data={
                            'samples': len(audio_data),
                            'sample_rate': self.sample_rate,
                        },
                        source='audio_capture',
                    ))
            
            except Exception as e:
                logger.error(f"Ошибка захвата звука: {e}")
                await asyncio.sleep(0.1)
    
    def _read_chunk(self) -> Optional[bytes]:
        """Чтение чанка данных (синхронно)"""
        if not self._stream:
            return None
        try:
            return self._stream.read(self.chunk_size, exception_on_overflow=False)
        except Exception as e:
            logger.debug(f"Ошибка чтения: {e}")
            return None
    
    async def stop(self) -> None:
        """Остановка захвата"""
        self._running = False
        
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        
        if self._stream:
            self._stream.stop_stream()
            self._stream.close()
        
        if self._pa:
            self._pa.terminate()
        
        logger.info("🛑 AudioCapture остановлен")
    
    def get_audio(self, seconds: float = 2.0) -> np.ndarray:
        """Получить последние N секунд аудио"""
        samples_needed = int(self.sample_rate * seconds)
        all_audio = self.ring_buffer.get_all()
        
        if len(all_audio) < samples_needed:
            return all_audio
        
        return all_audio[-samples_needed:]
