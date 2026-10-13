"""
Orchestrator — Оркестратор
Управляет потоком данных между компонентами
"""
import asyncio
import logging
import uuid
from typing import Any

from core.event_bus import EventBus, Event, EventType
from core.fsm import FSM, State

logger = logging.getLogger(__name__)


class Orchestrator:
    """
    Оркестратор — управляет потоком данных
    Координирует работу всех компонентов
    """
    
    def __init__(self, config: dict, event_bus: EventBus, fsm: FSM):
        self.config = config
        self.event_bus = event_bus
        self.fsm = fsm
        
        # Текущий request_id для трейсинга
        self._current_request_id: str = ""
        
        # История диалога
        self._conversation_history: list[dict] = []
        
        # Флаг работы
        self._running = False
        
        # Подключение компонентов (будут добавлены позже)
        self.audio_capture = None
        self.vad = None
        self.stt = None
        self.tts = None
        self.llm = None
        self.rag = None
        self.wake_word = None
        
        logger.info("Orchestrator инициализирован")
    
    async def start(self) -> None:
        """Запустить оркестратор"""
        self._running = True
        
        # Подписка на события
        self.event_bus.subscribe(EventType.TEXT_TRANSCRIBED, self._on_text_transcribed)
        self.event_bus.subscribe(EventType.STATE_CHANGED, self._on_state_changed)
        
        # Запуск компонентов (если они есть)
        if self.wake_word:
            await self.wake_word.start()
        if self.audio_capture:
            await self.audio_capture.start()
        if self.vad:
            await self.vad.start()
        
        logger.info("🚀 Orchestrator запущен")
    
    async def stop(self) -> None:
        """Остановить оркестратор"""
        self._running = False
        
        # Остановка компонентов
        if self.wake_word:
            await self.wake_word.stop()
        if self.audio_capture:
            await self.audio_capture.stop()
        if self.vad:
            await self.vad.stop()
        if self.stt:
            await self.stt.stop()
        if self.tts:
            await self.tts.stop()
        if self.llm:
            await self.llm.stop()
        
        logger.info("🛑 Orchestrator остановлен")
    
    async def _on_text_transcribed(self, event: Event) -> None:
        """Обработка распознанного текста"""
        if self.fsm.state != State.LISTEN:
            return
        
        user_text = event.data.get('text', '')
        if not user_text:
            return
        
        logger.info(f"📝 Пользователь: {user_text}")
        
        # Сохранение в историю
        self._conversation_history.append({
            'role': 'user',
            'content': user_text,
            'timestamp': event.timestamp.isoformat(),
        })
        
        # Переход в THINK
        await self.fsm.transition_to(State.THINK, "User text received")
        
        # Генерация ответа LLM
        await self._generate_response(user_text)
    
    async def _generate_response(self, user_text: str) -> None:
        """Генерация ответа с помощью LLM"""
        if not self.llm:
            logger.warning("LLM не подключен")
            return
        
        # Создание request_id для трейсинга
        self._current_request_id = str(uuid.uuid4())
        
        # Публикация события начала генерации
        await self.event_bus.publish(Event(
            type=EventType.LLM_THINKING,
            data={'user_text': user_text},
            source='orchestrator',
            request_id=self._current_request_id,
        ))
        
        try:
            # Поиск контекста в RAG (если есть)
            context = ""
            if self.rag:
                await self.event_bus.publish(Event(
                    type=EventType.RAG_SEARCHING,
                    data={'query': user_text},
                    source='orchestrator',
                    request_id=self._current_request_id,
                ))
                context = await self.rag.search(user_text)
                await self.event_bus.publish(Event(
                    type=EventType.RAG_CONTEXT_RETRIEVED,
                    data={'context_length': len(context)},
                    source='orchestrator',
                    request_id=self._current_request_id,
                ))
            
            # Генерация ответа
            response = await self.llm.generate(
                user_text=user_text,
                context=context,
                history=self._conversation_history[-10:],  # Последние 10 сообщений
            )
            
            # Сохранение в историю
            self._conversation_history.append({
                'role': 'assistant',
                'content': response,
                'timestamp': str(asyncio.get_event_loop().time()),
            })
            
            logger.info(f"🤖 Джарвис: {response}")
            
            # Публикация завершения генерации
            await self.event_bus.publish(Event(
                type=EventType.LLM_RESPONSE_COMPLETED,
                data={'response': response},
                source='orchestrator',
                request_id=self._current_request_id,
            ))
            
            # Переход в SPEAK
            await self.fsm.transition_to(State.SPEAK, "Response generated")
            
            # Озвучивание ответа
            if self.tts:
                await self.tts.speak(response)
        
        except Exception as e:
            logger.error(f"❌ Ошибка генерации ответа: {e}", exc_info=True)
            await self.event_bus.publish(Event(
                type=EventType.ERROR,
                data={'error': str(e), 'component': 'orchestrator'},
                source='orchestrator',
                request_id=self._current_request_id,
            ))
            # Возврат в IDLE
            await self.fsm.transition_to(State.IDLE, "Error during generation")
    
    async def _on_state_changed(self, event: Event) -> None:
        """Обработка изменения состояния"""
        new_state = event.data.get('new_state')
        logger.debug(f"📊 Состояние изменено: {new_state}")
        
        # Действия при переходе в определённые состояния
        if new_state == State.LISTEN:
            # Начинаем слушать
            if self.stt:
                await self.stt.start_listening()
        elif new_state == State.BARGE_IN:
            # Останавливаем TTS
            if self.tts:
                await self.tts.stop_speaking()
    
    @property
    def conversation_history(self) -> list[dict]:
        """История диалога"""
        return self._conversation_history.copy()
    
    def clear_history(self) -> None:
        """Очистить историю диалога"""
        self._conversation_history.clear()
        logger.info("🗑️ История диалога очищена")
