"""
FSM — Конечный автомат (Finite State Machine)
Управляет состояниями Джарвиса: IDLE → WAKE → LISTEN → THINK → SPEAK → BARGE_IN
"""
import asyncio
import logging
from enum import Enum
from typing import Callable, Coroutine, Any
from datetime import datetime

from core.event_bus import EventBus, Event, EventType

logger = logging.getLogger(__name__)


class State(str, Enum):
    """Состояния робота"""
    IDLE = "IDLE"          # Спит, ждёт wake word
    WAKE = "WAKE"          # Услышал wake word
    LISTEN = "LISTEN"      # Слушает пользователя
    THINK = "THINK"        # Думает (LLM генерирует ответ)
    SPEAK = "SPEAK"        # Говорит (TTS воспроизводит)
    BARGE_IN = "BARGE_IN"  # Перебит пользователем


# Допустимые переходы между состояниями
VALID_TRANSITIONS = {
    State.IDLE: [State.WAKE],
    State.WAKE: [State.LISTEN, State.IDLE],
    State.LISTEN: [State.THINK, State.IDLE, State.BARGE_IN],
    State.THINK: [State.SPEAK, State.IDLE, State.BARGE_IN],
    State.SPEAK: [State.IDLE, State.BARGE_IN, State.LISTEN],
    State.BARGE_IN: [State.LISTEN, State.IDLE],
}


class FSM:
    """
    Конечный автомат
    Управляет потоком состояний робота
    """
    
    def __init__(self, config: dict, event_bus: EventBus):
        self.config = config
        self.event_bus = event_bus
        
        # Текущее состояние
        initial_state = config.get('initial_state', 'IDLE')
        self._state = State(initial_state)
        
        # История состояний
        self._history: list[tuple[State, datetime]] = [(self._state, datetime.now())]
        
        # Callbacks для переходов
        self._on_enter: dict[State, Callable] = {}
        self._on_exit: dict[State, Callable] = {}
        
        # Подписка на события
        self._setup_event_handlers()
        
        logger.info(f"FSM инициализирован (начальное состояние: {self._state.value})")
    
    def _setup_event_handlers(self) -> None:
        """Настройка обработчиков событий"""
        self.event_bus.subscribe(EventType.WAKE_DETECTED, self._on_wake_detected)
        self.event_bus.subscribe(EventType.SPEECH_ENDED, self._on_speech_ended)
        self.event_bus.subscribe(EventType.LLM_RESPONSE_COMPLETED, self._on_llm_completed)
        self.event_bus.subscribe(EventType.TTS_COMPLETED, self._on_tts_completed)
        self.event_bus.subscribe(EventType.SPEECH_DETECTED, self._on_speech_during_speak)
    
    @property
    def state(self) -> State:
        """Текущее состояние"""
        return self._state
    
    async def transition_to(self, new_state: State, reason: str = "") -> bool:
        """
        Переход в новое состояние
        Возвращает True если переход успешен
        """
        # Проверка допустимости перехода
        if new_state not in VALID_TRANSITIONS.get(self._state, []):
            logger.warning(
                f"⚠️ Недопустимый переход: {self._state.value} → {new_state.value} "
                f"(причина: {reason})"
            )
            return False
        
        old_state = self._state
        
        # Вызов on_exit для старого состояния
        if old_state in self._on_exit:
            try:
                await self._on_exit[old_state]()
            except Exception as e:
                logger.error(f"Ошибка on_exit для {old_state.value}: {e}")
        
        # Переход
        self._state = new_state
        self._history.append((new_state, datetime.now()))
        
        logger.info(f"🔄 FSM: {old_state.value} → {new_state.value} ({reason})")
        
        # Публикация события
        await self.event_bus.publish(Event(
            type=EventType.STATE_CHANGED,
            data={
                'old_state': old_state.value,
                'new_state': new_state.value,
                'reason': reason,
            },
            source='fsm',
        ))
        
        # Вызов on_enter для нового состояния
        if new_state in self._on_enter:
            try:
                await self._on_enter[new_state]()
            except Exception as e:
                logger.error(f"Ошибка on_enter для {new_state.value}: {e}")
        
        return True
    
    def on_enter(self, state: State):
        """Декоратор для регистрации callback при входе в состояние"""
        def decorator(func: Callable):
            self._on_enter[state] = func
            return func
        return decorator
    
    def on_exit(self, state: State):
        """Декоратор для регистрации callback при выходе из состояния"""
        def decorator(func: Callable):
            self._on_exit[state] = func
            return func
        return decorator
    
    # Обработчики событий
    
    async def _on_wake_detected(self, event: Event) -> None:
        """Обработка wake word"""
        if self._state == State.IDLE:
            await self.transition_to(State.WAKE, "Wake word detected")
            # Автоматический переход в LISTEN
            await asyncio.sleep(0.1)
            await self.transition_to(State.LISTEN, "Ready to listen")
    
    async def _on_speech_ended(self, event: Event) -> None:
        """Обработка окончания речи пользователя"""
        if self._state == State.LISTEN:
            await self.transition_to(State.THINK, "User finished speaking")
    
    async def _on_llm_completed(self, event: Event) -> None:
        """Обработка завершения генерации ответа LLM"""
        if self._state == State.THINK:
            await self.transition_to(State.SPEAK, "LLM response ready")
    
    async def _on_tts_completed(self, event: Event) -> None:
        """Обработка завершения воспроизведения TTS"""
        if self._state == State.SPEAK:
            await self.transition_to(State.IDLE, "TTS completed")
    
    async def _on_speech_during_speak(self, event: Event) -> None:
        """Обработка речи во время SPEAK (barge-in)"""
        if self._state == State.SPEAK:
            await self.transition_to(State.BARGE_IN, "User interrupted")
            # Возврат к слушанию
            await asyncio.sleep(0.1)
            await self.transition_to(State.LISTEN, "Listening after barge-in")
    
    @property
    def history(self) -> list[tuple[State, datetime]]:
        """История состояний"""
        return self._history.copy()
    
    def get_state_duration(self) -> float:
        """Время в текущем состоянии (секунды)"""
        if not self._history:
            return 0.0
        last_time = self._history[-1][1]
        return (datetime.now() - last_time).total_seconds()
