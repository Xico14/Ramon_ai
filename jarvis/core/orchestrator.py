"""
Orchestrator — Оркестратор (Фаза 4.5: AEC + Barge-in)
Управляет потоком данных между компонентами
Включает AEC и улучшенный Barge-in
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
    Включает AEC (подавление эхо) и Barge-in
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
        self.aec = None  # НОВОЕ: AEC для подавления эхо
        
        # Barge-in параметры
        self._barge_in_threshold = config.get('barge_in_threshold', 0.5)
        self._barge_in_enabled = True
        
        logger.info("Orchestrator инициализирован (с AEC и Barge-in)")
    
    async def start(self) -> None:
        """Запустить оркестратор"""
        self._running = True
        
        # Подписка на события
        self.event_bus.subscribe(EventType.TEXT_TRANSCRIBED, self._on_text_transcribed)
        self.event_bus.subscribe(EventType.STATE_CHANGED, self._on_state_changed)
        self.event_bus.subscribe(EventType.SPEECH_DETECTED, self._on_speech_detected)
        self.event_bus.subscribe(EventType.AUDIO_CAPTURED, self._on_audio_captured)
        
        # Запуск компонентов (если они есть)
        if self.aec:
            await self.aec.start()
            logger.info("✅ AEC запущен")
        
        if self.wake_word:
            await self.wake_word.start()
        if self.audio_capture:
            await self.audio_capture.start()
        if self.vad:
            await self.vad.start()
        
        logger.info("🚀 Orchestrator запущен (с AEC и Barge-in)")
    
    async def stop(self) -> None:
        """Остановить оркестратор"""
        self._running = False
        
        # Остановка компонентов
        if self.aec:
            await self.aec.stop()
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
    
    async def _on_audio_captured(self, event: Event) -> None:
        """
        Обработка захваченного аудио
        Применяет AEC если активно воспроизведение
        """
        if not self.aec or not self._running:
            return
        
        # Если TTS активен, применяем AEC
        if self.tts and self.tts.is_speaking:
            # Получаем reference signal (то, что воспроизводится)
            # В реальной реализации это будет буферизованный аудио с TTS
            # Пока это заглушка
            pass
    
    async def _on_speech_detected(self, event: Event) -> None:
        """
        Обработка обнаружения речи
        Barge-in: если робот говорит и пользователь начал говорить
        """
        if not self._barge_in_enabled:
            return
        
        # Проверяем состояние FSM
        current_state = self.fsm.state
        
        # Если робот говорит (SPEAK) и обнаружена речь пользователя
        if current_state == State.SPEAK:
            logger.info("🛑 BARGE-IN: Пользователь перебивает робота!")
            
            # Немедленно останавливаем TTS
            if self.tts:
                await self.tts.stop_speaking()
            
            # Переход в состояние BARGE_IN
            await self.fsm.transition_to(State.BARGE_IN, "User interrupted (barge-in)")
            
            # Публикуем событие
            await self.event_bus.publish(Event(
                type=EventType.SPEECH_DETECTED,
                data={'barge_in': True},
                source='orchestrator',
            ))
    
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
            # Возврат к слушанию
            await asyncio.sleep(0.1)
            await self.fsm.transition_to(State.LISTEN, "Listening after barge-in")
    
    @property
    def conversation_history(self) -> list[dict]:
        """История диалога"""
        return self._conversation_history.copy()
    
    def clear_history(self) -> None:
        """Очистить историю диалога"""
        self._conversation_history.clear()
        logger.info("🗑️ История диалога очищена")
    
    @property
    def aec_stats(self) -> dict:
        """Статистика AEC"""
        if self.aec:
            return {
                'enabled': self.aec.is_active,
                'erle_db': self.aec.erle_db,
            }
        return {'enabled': False, 'erle_db': 0.0}
