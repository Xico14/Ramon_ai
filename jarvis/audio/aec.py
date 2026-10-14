"""
AEC — Acoustic Echo Cancellation (Подавление эхо)
WebRTC AEC для устранения эхо от динамика в микрофоне
"""
import asyncio
import logging
import numpy as np
from typing import Optional

from core.event_bus import EventBus, Event, EventType

logger = logging.getLogger(__name__)


class AEC:
    """
    Acoustic Echo Cancellation
    Подавляет эхо от динамика в сигнале микрофона
    """
    
    def __init__(self, config: dict, event_bus: EventBus):
        self.config = config
        self.event_bus = event_bus
        
        # Параметры AEC
        self.filter_length = config.get('filter_length', 2048)  # Длина фильтра
        self.mu = config.get('mu', 0.01)  # Шаг адаптации
        self.enabled = config.get('enabled', True)
        
        # Состояние
        self._running = False
        self._reference_signal: Optional[np.ndarray] = None  # Сигнал с динамика
        self._error_signal: Optional[np.ndarray] = None  # Ошибка эхо
        
        # Адаптивный фильтр (NLMS - Normalized Least Mean Squares)
        self._filter_coeffs: Optional[np.ndarray] = None
        
        # Буферы
        self._mic_buffer = np.zeros(self.filter_length, dtype=np.float32)
        self._ref_buffer = np.zeros(self.filter_length, dtype=np.float32)
        
        # Статистика
        self._erle = 0.0  # Echo Return Loss Enhancement (dB)
        
        logger.info(f"AEC инициализирован (filter_length={self.filter_length})")
    
    async def start(self) -> None:
        """Запуск AEC"""
        if not self.enabled:
            logger.info("⚠️ AEC отключен в конфигурации")
            return
        
        # Инициализация фильтра
        self._filter_coeffs = np.zeros(self.filter_length, dtype=np.float32)
        
        # Подписка на события
        self.event_bus.subscribe(EventType.AUDIO_PLAYBACK_STARTED, self._on_playback_started)
        self.event_bus.subscribe(EventType.AUDIO_PLAYBACK_STOPPED, self._on_playback_stopped)
        
        self._running = True
        logger.info("🔇 AEC запущен")
    
    async def _on_playback_started(self, event: Event) -> None:
        """Обработка начала воспроизведения"""
        logger.debug("🔊 Воспроизведение началось — AEC активен")
    
    async def _on_playback_stopped(self, event: Event) -> None:
        """Обработка остановки воспроизведения"""
        logger.debug("🔇 Воспроизведение остановлено — AEC неактивен")
    
    def set_reference_signal(self, signal: np.ndarray) -> None:
        """
        Установить reference signal (сигнал с динамика)
        Это то, что робот воспроизводит
        """
        self._reference_signal = signal
        # Обновление буфера
        self._ref_buffer = np.roll(self._ref_buffer, -len(signal))
        self._ref_buffer[-len(signal):] = signal
    
    def process(self, mic_signal: np.ndarray) -> np.ndarray:
        """
        Обработка сигнала микрофона с подавлением эхо
        
        Args:
            mic_signal: Сигнал с микрофона
        
        Returns:
            Очищенный сигнал (без эхо)
        """
        if not self.enabled or self._reference_signal is None:
            return mic_signal
        
        # Обновление буфера микрофона
        self._mic_buffer = np.roll(self._mic_buffer, -len(mic_signal))
        self._mic_buffer[-len(mic_signal):] = mic_signal
        
        # Оценка эхо с помощью адаптивного фильтра
        echo_estimate = np.convolve(self._ref_buffer, self._filter_coeffs, mode='valid')
        
        # Вычитание эхо из сигнала микрофона
        if len(echo_estimate) >= len(mic_signal):
            echo_estimate = echo_estimate[-len(mic_signal):]
        else:
            # Дополняем нулями
            echo_estimate = np.pad(echo_estimate, (len(mic_signal) - len(echo_estimate), 0))
        
        # Очищенный сигнал
        cleaned_signal = mic_signal - echo_estimate
        
        # Обновление коэффициентов фильтра (NLMS алгоритм)
        self._update_filter(mic_signal, echo_estimate, cleaned_signal)
        
        # Вычисление ERLE (Echo Return Loss Enhancement)
        self._calculate_erle(mic_signal, cleaned_signal)
        
        return cleaned_signal
    
    def _update_filter(
        self,
        mic_signal: np.ndarray,
        echo_estimate: np.ndarray,
        error_signal: np.ndarray
    ) -> None:
        """
        Обновление коэффициентов адаптивного фильтра (NLMS)
        
        NLMS: w(n+1) = w(n) + mu * e(n) * x(n) / (x(n)^T * x(n) + epsilon)
        """
        # Мощность reference signal
        ref_power = np.sum(self._ref_buffer ** 2) + 1e-10  # Избегаем деления на 0
        
        # Обновление коэффициентов
        gradient = self.mu * error_signal[-1] * self._ref_buffer / ref_power
        self._filter_coeffs += gradient
    
    def _calculate_erle(self, original: np.ndarray, cleaned: np.ndarray) -> None:
        """
        Вычисление Echo Return Loss Enhancement (ERLE)
        ERLE = 10 * log10(P_original / P_cleaned)
        """
        power_original = np.mean(original ** 2) + 1e-10
        power_cleaned = np.mean(cleaned ** 2) + 1e-10
        
        if power_cleaned > 0:
            self._erle = 10 * np.log10(power_original / power_cleaned)
        else:
            self._erle = 0.0
    
    async def stop(self) -> None:
        """Остановка AEC"""
        self._running = False
        self._reference_signal = None
        
        # Отписка от событий
        self.event_bus.unsubscribe(EventType.AUDIO_PLAYBACK_STARTED, self._on_playback_started)
        self.event_bus.unsubscribe(EventType.AUDIO_PLAYBACK_STOPPED, self._on_playback_stopped)
        
        logger.info("🛑 AEC остановлен")
    
    @property
    def erle_db(self) -> float:
        """Echo Return Loss Enhancement в dB"""
        return self._erle
    
    @property
    def is_active(self) -> bool:
        """Активен ли AEC"""
        return self._running and self._reference_signal is not None
