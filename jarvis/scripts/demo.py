"""
Демо-режим Джарвиса
Запуск без реального аудио (для тестирования UI и FSM)
"""
import asyncio
import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.event_bus import EventBus, Event, EventType
from core.fsm import FSM, State
from core.orchestrator import Orchestrator
from core.config import load_config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def demo_mode():
    """Демо-режим с имитацией событий"""
    
    logger.info("=" * 60)
    logger.info("🤖 ДЖАРВИС — ДЕМО РЕЖИМ")
    logger.info("=" * 60)
    logger.info("Имитация голосового диалога без реального аудио")
    logger.info("=" * 60)
    
    # Загрузка конфигурации
    config = load_config('./config.yaml')
    
    # Создание компонентов
    event_bus = EventBus(config['event_bus'])
    fsm = FSM(config['fsm'], event_bus)
    orchestrator = Orchestrator(config, event_bus, fsm)
    
    # Запуск Event Bus
    await event_bus.start()
    
    logger.info("\n📊 Начальное состояние: IDLE (Спит)")
    logger.info("-" * 60)
    
    # Имитация диалога
    demo_scenario = [
        {
            'delay': 2,
            'event': EventType.WAKE_DETECTED,
            'data': {'word': 'demo'},
            'description': '🔔 Wake Word обнаружен ("Джарвис")',
        },
        {
            'delay': 1,
            'event': EventType.SPEECH_DETECTED,
            'data': {},
            'description': '🎤 Пользователь начал говорить',
        },
        {
            'delay': 2,
            'event': EventType.SPEECH_ENDED,
            'data': {'duration_ms': 2000},
            'description': '🔇 Пользователь закончил говорить',
        },
        {
            'delay': 1,
            'event': EventType.TEXT_TRANSCRIBED,
            'data': {'text': 'Привет, Джарвис! Как дела?'},
            'description': '📝 Распознанный текст: "Привет, Джарвис! Как дела?"',
        },
        {
            'delay': 2,
            'event': EventType.LLM_THINKING,
            'data': {'user_text': 'Привет, Джарвис! Как дела?'},
            'description': '💭 LLM думает...',
        },
        {
            'delay': 3,
            'event': EventType.LLM_RESPONSE_COMPLETED,
            'data': {'response': 'Привет! У меня всё отлично, спасибо. Чем могу помочь?'},
            'description': '✅ LLM сгенерировал ответ',
        },
        {
            'delay': 1,
            'event': EventType.TTS_GENERATING,
            'data': {'text': 'Привет! У меня всё отлично, спасибо. Чем могу помочь?'},
            'description': '🔊 TTS генерирует речь',
        },
        {
            'delay': 2,
            'event': EventType.TTS_SPEAKING,
            'data': {'samples': 48000},
            'description': '🗣️ Джарвис говорит',
        },
        {
            'delay': 3,
            'event': EventType.TTS_COMPLETED,
            'data': {'text': 'Привет! У меня всё отлично, спасибо. Чем могу помочь?'},
            'description': '✅ TTS завершён',
        },
    ]
    
    # Выполнение сценария
    for step in demo_scenario:
        await asyncio.sleep(step['delay'])
        
        logger.info(f"\n{step['description']}")
        logger.info(f"   Состояние FSM: {fsm.state.value}")
        
        event = Event(
            type=step['event'],
            data=step['data'],
            source='demo',
        )
        await event_bus.publish(event)
        
        # Даём время на обработку
        await asyncio.sleep(0.1)
    
    # Имитация barge-in
    logger.info("\n" + "=" * 60)
    logger.info("🛑 ТЕСТ BARGE-IN (перебивание)")
    logger.info("=" * 60)
    
    await asyncio.sleep(2)
    logger.info("\n🗣️ Джарвис говорит...")
    await event_bus.publish(Event(
        type=EventType.TTS_SPEAKING,
        data={'samples': 48000},
        source='demo',
    ))
    
    await asyncio.sleep(1)
    logger.info("\n👤 Пользователь перебивает!")
    await event_bus.publish(Event(
        type=EventType.SPEECH_DETECTED,
        data={},
        source='demo',
    ))
    
    await asyncio.sleep(0.5)
    logger.info(f"   Состояние FSM: {fsm.state.value}")
    
    # Финальная статистика
    await asyncio.sleep(2)
    
    logger.info("\n" + "=" * 60)
    logger.info("📊 СТАТИСТИКА ДЕМО")
    logger.info("=" * 60)
    
    stats = event_bus.stats
    logger.info(f"   Событий опубликовано: {stats['published']}")
    logger.info(f"   Событий доставлено: {stats['delivered']}")
    logger.info(f"   Ошибок: {stats['failed']}")
    logger.info(f"   Подписчиков: {stats['subscribers']}")
    
    logger.info(f"\n   История состояний FSM:")
    for state, timestamp in fsm.history:
        logger.info(f"   - {state.value} ({timestamp.strftime('%H:%M:%S')})")
    
    # Остановка
    await event_bus.stop()
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ ДЕМО ЗАВЕРШЕНО")
    logger.info("=" * 60)
    logger.info("\nСледующие шаги:")
    logger.info("1. Запустите полный режим: python main.py")
    logger.info("2. Скажите 'Джарвис' для активации")
    logger.info("3. Задайте вопрос")


if __name__ == '__main__':
    try:
        asyncio.run(demo_mode())
    except KeyboardInterrupt:
        logger.info("\n\n🛑 Демо остановлено пользователем")
    except Exception as e:
        logger.error(f"\n❌ Ошибка: {e}", exc_info=True)
