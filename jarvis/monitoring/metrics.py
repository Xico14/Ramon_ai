"""
Metrics Collector — Сбор метрик
CPU, RAM, latency, event bus statistics
"""
import asyncio
import logging
import time
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from collections import deque
import psutil
import os

logger = logging.getLogger(__name__)


@dataclass
class MetricPoint:
    """Точка метрики"""
    timestamp: float
    value: float
    label: str = ""


@dataclass
class MetricsSnapshot:
    """Снимок метрик"""
    timestamp: float
    cpu_percent: float
    ram_used_mb: float
    ram_total_mb: float
    ram_percent: float
    event_bus_published: int
    event_bus_delivered: int
    event_bus_failed: int
    event_bus_queue_size: int
    fsm_state: str
    active_components: List[str]
    custom_metrics: Dict[str, float] = field(default_factory=dict)


class MetricsCollector:
    """
    Сборщик метрик
    Собирает CPU, RAM, latency, event bus statistics
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.collection_interval = config.get('collection_interval', 5.0)  # секунды
        self.history_size = config.get('history_size', 1000)  # количество точек
        
        # История метрик
        self._cpu_history: deque[MetricPoint] = deque(maxlen=self.history_size)
        self._ram_history: deque[MetricPoint] = deque(maxlen=self.history_size)
        self._latency_history: Dict[str, deque[MetricPoint]] = {}
        
        # Ссылки на компоненты
        self._event_bus = None
        self._fsm = None
        self._orchestrator = None
        
        # Задача сбора
        self._running = False
        self._task: Optional[asyncio.Task] = None
        
        # Кастомные метрики
        self._custom_metrics: Dict[str, float] = {}
        
        logger.info(f"MetricsCollector инициализирован (interval={self.collection_interval}s)")
    
    def set_components(self, event_bus=None, fsm=None, orchestrator=None):
        """Установка ссылок на компоненты для сбора их метрик"""
        self._event_bus = event_bus
        self._fsm = fsm
        self._orchestrator = orchestrator
        logger.info("✅ Компоненты подключены к сборщику метрик")
    
    async def start(self) -> None:
        """Запуск сбора метрик"""
        self._running = True
        self._task = asyncio.create_task(self._collection_loop())
        logger.info("📊 MetricsCollector запущен")
    
    async def _collection_loop(self) -> None:
        """Цикл сбора метрик"""
        while self._running:
            try:
                await self._collect_metrics()
                await asyncio.sleep(self.collection_interval)
            except Exception as e:
                logger.error(f"Ошибка сбора метрик: {e}")
                await asyncio.sleep(self.collection_interval)
    
    async def _collect_metrics(self) -> None:
        """Сбор метрик"""
        timestamp = time.time()
        
        # CPU и RAM
        process = psutil.Process(os.getpid())
        cpu_percent = process.cpu_percent()
        ram_info = process.memory_info()
        ram_used_mb = ram_info.rss / 1024 / 1024
        
        system_ram = psutil.virtual_memory()
        ram_total_mb = system_ram.total / 1024 / 1024
        ram_percent = system_ram.percent
        
        # Сохранение в историю
        self._cpu_history.append(MetricPoint(timestamp, cpu_percent))
        self._ram_history.append(MetricPoint(timestamp, ram_used_mb))
        
        # Event Bus метрики
        event_bus_metrics = {}
        if self._event_bus:
            stats = self._event_bus.stats
            event_bus_metrics = {
                'published': stats['published'],
                'delivered': stats['delivered'],
                'failed': stats['failed'],
                'queue_size': stats['queue_size'],
            }
        
        # FSM состояние
        fsm_state = self._fsm.state.value if self._fsm else "UNKNOWN"
        
        # Активные компоненты
        active_components = []
        if self._orchestrator:
            if self._orchestrator.audio_capture:
                active_components.append('audio_capture')
            if self._orchestrator.vad:
                active_components.append('vad')
            if self._orchestrator.stt:
                active_components.append('stt')
            if self._orchestrator.tts:
                active_components.append('tts')
            if self._orchestrator.llm:
                active_components.append('llm')
            if self._orchestrator.rag:
                active_components.append('rag')
        
        # Логирование (каждые 30 секунд)
        if int(timestamp) % 30 == 0:
            logger.info(
                f"📊 Метрики: CPU={cpu_percent:.1f}%, "
                f"RAM={ram_used_mb:.0f}MB ({ram_percent:.1f}%), "
                f"Events={event_bus_metrics.get('published', 0)}"
            )
    
    def record_latency(self, component: str, latency_ms: float) -> None:
        """
        Запись latency компонента
        
        Args:
            component: Название компонента (stt, tts, llm, rag)
            latency_ms: Задержка в миллисекундах
        """
        if component not in self._latency_history:
            self._latency_history[component] = deque(maxlen=self.history_size)
        
        self._latency_history[component].append(
            MetricPoint(time.time(), latency_ms, component)
        )
    
    def set_custom_metric(self, name: str, value: float) -> None:
        """
        Установка кастомной метрики
        
        Args:
            name: Название метрики
            value: Значение
        """
        self._custom_metrics[name] = value
    
    def get_snapshot(self) -> MetricsSnapshot:
        """
        Получение снимка текущих метрик
        
        Returns:
            MetricsSnapshot с текущими значениями
        """
        process = psutil.Process(os.getpid())
        
        # Текущие значения
        cpu_percent = process.cpu_percent()
        ram_info = process.memory_info()
        ram_used_mb = ram_info.rss / 1024 / 1024
        
        system_ram = psutil.virtual_memory()
        ram_total_mb = system_ram.total / 1024 / 1024
        ram_percent = system_ram.percent
        
        # Event Bus метрики
        event_bus_published = 0
        event_bus_delivered = 0
        event_bus_failed = 0
        event_bus_queue_size = 0
        
        if self._event_bus:
            stats = self._event_bus.stats
            event_bus_published = stats['published']
            event_bus_delivered = stats['delivered']
            event_bus_failed = stats['failed']
            event_bus_queue_size = stats['queue_size']
        
        # FSM состояние
        fsm_state = self._fsm.state.value if self._fsm else "UNKNOWN"
        
        # Активные компоненты
        active_components = []
        if self._orchestrator:
            if self._orchestrator.audio_capture:
                active_components.append('audio_capture')
            if self._orchestrator.vad:
                active_components.append('vad')
            if self._orchestrator.stt:
                active_components.append('stt')
            if self._orchestrator.tts:
                active_components.append('tts')
            if self._orchestrator.llm:
                active_components.append('llm')
            if self._orchestrator.rag:
                active_components.append('rag')
        
        return MetricsSnapshot(
            timestamp=time.time(),
            cpu_percent=cpu_percent,
            ram_used_mb=ram_used_mb,
            ram_total_mb=ram_total_mb,
            ram_percent=ram_percent,
            event_bus_published=event_bus_published,
            event_bus_delivered=event_bus_delivered,
            event_bus_failed=event_bus_failed,
            event_bus_queue_size=event_bus_queue_size,
            fsm_state=fsm_state,
            active_components=active_components,
            custom_metrics=self._custom_metrics.copy()
        )
    
    def get_cpu_stats(self) -> Dict:
        """Статистика CPU"""
        if not self._cpu_history:
            return {'avg': 0.0, 'min': 0.0, 'max': 0.0, 'current': 0.0}
        
        values = [p.value for p in self._cpu_history]
        return {
            'avg': sum(values) / len(values),
            'min': min(values),
            'max': max(values),
            'current': values[-1],
            'samples': len(values)
        }
    
    def get_ram_stats(self) -> Dict:
        """Статистика RAM"""
        if not self._ram_history:
            return {'avg': 0.0, 'min': 0.0, 'max': 0.0, 'current': 0.0}
        
        values = [p.value for p in self._ram_history]
        return {
            'avg': sum(values) / len(values),
            'min': min(values),
            'max': max(values),
            'current': values[-1],
            'samples': len(values)
        }
    
    def get_latency_stats(self, component: str) -> Dict:
        """Статистика latency компонента"""
        if component not in self._latency_history or not self._latency_history[component]:
            return {'avg': 0.0, 'min': 0.0, 'max': 0.0, 'current': 0.0, 'p95': 0.0}
        
        values = [p.value for p in self._latency_history[component]]
        values_sorted = sorted(values)
        p95_index = int(len(values_sorted) * 0.95)
        
        return {
            'avg': sum(values) / len(values),
            'min': min(values),
            'max': max(values),
            'current': values[-1],
            'p95': values_sorted[p95_index] if values_sorted else 0.0,
            'samples': len(values)
        }
    
    async def stop(self) -> None:
        """Остановка сбора метрик"""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("🛑 MetricsCollector остановлен")
    
    @property
    def is_running(self) -> bool:
        """Запущен ли сборщик"""
        return self._running
