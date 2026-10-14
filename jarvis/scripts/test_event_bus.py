"""
Простой тест EventBus без Qt
Проверяет работу шины событий в чистом asyncio
"""
import asyncio
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.event_bus import EventBus, Event, EventType

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def test_event_bus():
    """Тест EventBus"""
    logger.info("=" * 60)
    logger.info("🧪 ТЕСТ EVENT BUS")
    logger.info("=" * 60)
    
    # Создание EventBus
    config = {
        'max_queue_size': 100,
        'dlq_path': './data/test_dlq.json'
    }
    
    event_bus = EventBus(config)
    logger.info("✅ EventBus создан")
    
    # Счётчик полученных событий
    received_events = []
    
    # Обработчик событий
    async def test_handler(event: Event):
        logger.info(f"📨 Получено событие: {event.type.value}")
        received_events.append(event)
    
    # Подписка
    event_bus.subscribe(EventType.WAKE_DETECTED, test_handler)
    logger.info("✅ Подписка оформлена")
    
    # Запуск EventBus
    await event_bus.start()
    logger.info("✅ EventBus запущен")
    
    # Публикация событий
    for i in range(5):
        event = Event(
            type=EventType.WAKE_DETECTED,
            data={'test': i},
            source='test'
        )
        await event_bus.publish(event)
        logger.info(f"📤 Событие {i+1} опубликовано")
        await asyncio.sleep(0.1)
    
    # Ожидание обработки
    await asyncio.sleep(0.5)
    
    # Проверка результатов
    logger.info(f"\n📊 Получено событий: {len(received_events)}")
    
    # Статистика
    stats = event_bus.stats
    logger.info(f"📈 Статистика:")
    logger.info(f"   Опубликовано: {stats['published']}")
    logger.info(f"   Доставлено: {stats['delivered']}")
    logger.info(f"   Ошибок: {stats['failed']}")
    logger.info(f"   В очереди: {stats['queue_size']}")
    
    # Остановка
    await event_bus.stop()
    logger.info("✅ EventBus остановлен")
    
    # Проверка
    if len(received_events) == 5:
        logger.info("\n✅ ТЕСТ ПРОЙДЕН: Все события доставлены")
        return True
    else:
        logger.error(f"\n❌ ТЕСТ ПРОВАЛЕН: Ожидалось 5 событий, получено {len(received_events)}")
        return False


async def main():
    """Главная функция"""
    try:
        success = await test_event_bus()
        return 0 if success else 1
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
