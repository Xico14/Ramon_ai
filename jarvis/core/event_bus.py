"""
Event Bus — Нервная система Джарвиса
Центральная шина событий для коммуникации между компонентами
"""
import asyncio
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Coroutine
from collections import defaultdict

logger = logging.getLogger(__name__)


class EventType(str, Enum):
    """Типы событий в системе"""
    # Audio events
    AUDIO_CAPTURED = "audio.captured"
    AUDIO_PLAYBACK_STARTED = "audio.playback.started"
    AUDIO_PLAYBACK_STOPPED = "audio.playback.stopped"
    
    # Speech events
    SPEECH_DETECTED = "speech.detected"
    SPEECH_ENDED = "speech.ended"
    TEXT_TRANSCRIBED = "text.transcribed"
    
    # Wake word events
    WAKE_DETECTED = "wake.detected"
    
    # LLM events
    LLM_THINKING = "llm.thinking"
    LLM_RESPONSE_STARTED = "llm.response.started"
    LLM_TOKEN_GENERATED = "llm.token.generated"
    LLM_RESPONSE_COMPLETED = "llm.response.completed"
    
    # TTS events
    TTS_GENERATING = "tts.generating"
    TTS_SPEAKING = "tts.speaking"
    TTS_COMPLETED = "tts.completed"
    
    # RAG events
    RAG_SEARCHING = "rag.searching"
    RAG_CONTEXT_RETRIEVED = "rag.context.retrieved"
    
    # FSM events
    STATE_CHANGED = "fsm.state.changed"
    
    # Tool events
    TOOL_CALL_REQUESTED = "tool.call.requested"
    TOOL_CALL_COMPLETED = "tool.call.completed"
    
    # System events
    ERROR = "system.error"
    HEALTH_CHECK = "system.health_check"
    SHUTDOWN = "system.shutdown"


@dataclass
class Event:
    """Событие в системе"""
    type: EventType
    data: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = ""
    request_id: str = ""  # Для трейсинга
    
    def to_dict(self) -> dict:
        return {
            'type': self.type.value,
            'data': self.data,
            'timestamp': self.timestamp.isoformat(),
            'source': self.source,
            'request_id': self.request_id,
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)


# Тип обработчика событий
EventHandler = Callable[[Event], Coroutine[Any, Any, None]]


class EventBus:
    """
    Центральная шина событий
    Все компоненты общаются только через неё
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.max_queue_size = config.get('max_queue_size', 1000)
        self.dlq_path = Path(config.get('dlq_path', './data/dlq.json'))
        
        # Подписчики: event_type -> [handlers]
        self._subscribers: dict[EventType, list[EventHandler]] = defaultdict(list)
        
        # Очередь событий (создаётся лениво при start())
        self._queue: asyncio.Queue | None = None
        
        # Dead Letter Queue (для недоставленных событий)
        self._dlq: list[Event] = []
        
        # Статистика
        self._events_published = 0
        self._events_delivered = 0
        self._events_failed = 0
        
        # Флаг работы
        self._running = False
        self._task: asyncio.Task | None = None
        
        logger.info(f"EventBus инициализирован (max_queue={self.max_queue_size})")
    
    def subscribe(self, event_type: EventType, handler: EventHandler) -> None:
        """Подписаться на событие"""
        self._subscribers[event_type].append(handler)
        logger.debug(f"Подписка: {handler.__name__} → {event_type.value}")
    
    def unsubscribe(self, event_type: EventType, handler: EventHandler) -> None:
        """Отписаться от события"""
        if handler in self._subscribers[event_type]:
            self._subscribers[event_type].remove(handler)
            logger.debug(f"Отписка: {handler.__name__} ← {event_type.value}")
    
    async def publish(self, event: Event) -> None:
        """Опубликовать событие"""
        self._events_published += 1
        
        # Ленивая инициализация queue
        if self._queue is None:
            self._queue = asyncio.Queue(maxsize=self.max_queue_size)
        
        try:
            self._queue.put_nowait(event)
            logger.debug(f"📤 Событие опубликовано: {event.type.value} (от {event.source})")
        except asyncio.QueueFull:
            logger.warning(f"⚠️ Очередь событий переполнена! Событие в DLQ: {event.type.value}")
            self._add_to_dlq(event)
    
    async def _process_events(self) -> None:
        """Обработка событий из очереди"""
        # Ленивая инициализация queue
        if self._queue is None:
            self._queue = asyncio.Queue(maxsize=self.max_queue_size)
        
        while self._running:
            try:
                event = await asyncio.wait_for(self._queue.get(), timeout=1.0)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Ошибка получения события: {e}")
                continue
            
            # Доставляем событие всем подписчикам
            handlers = self._subscribers.get(event.type, [])
            
            for handler in handlers:
                try:
                    await handler(event)
                    self._events_delivered += 1
                except Exception as e:
                    self._events_failed += 1
                    logger.error(f"❌ Ошибка обработчика {handler.__name__}: {e}", exc_info=True)
                    self._add_to_dlq(event)
    
    def _add_to_dlq(self, event: Event) -> None:
        """Добавить событие в Dead Letter Queue"""
        self._dlq.append(event)
        
        # Сохраняем DLQ на диск
        try:
            dlq_data = [e.to_dict() for e in self._dlq[-100:]]  # Последние 100
            self.dlq_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.dlq_path, 'w', encoding='utf-8') as f:
                json.dump(dlq_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Ошибка сохранения DLQ: {e}")
    
    async def start(self) -> None:
        """Запустить обработку событий"""
        self._running = True
        self._task = asyncio.create_task(self._process_events())
        logger.info("📡 Event Bus запущен")
    
    async def stop(self) -> None:
        """Остановить обработку событий"""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        # Очищаем queue
        if self._queue:
            while not self._queue.empty():
                try:
                    self._queue.get_nowait()
                except:
                    break
        logger.info("📡 Event Bus остановлен")
    
    @property
    def stats(self) -> dict:
        """Статистика шины событий"""
        return {
            'published': self._events_published,
            'delivered': self._events_delivered,
            'failed': self._events_failed,
            'dlq_size': len(self._dlq),
            'queue_size': self._queue.qsize() if self._queue else 0,
            'subscribers': sum(len(h) for h in self._subscribers.values()),
        }
