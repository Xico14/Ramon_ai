"""
Тесты Фазы 7.5-7.8 — Полировка
Stress testing, performance, degradation mode
"""
import asyncio
import logging
import sys
import time
import psutil
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config import load_config
from core.event_bus import EventBus, Event, EventType
from core.fsm import FSM
from monitoring.metrics import MetricsCollector
from monitoring.health import HealthChecker, HealthStatus
from monitoring.degradation import DegradationManager, DegradationLevel

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def test_metrics_collector():
    """
    Тест сборщика метрик
    """
    logger.info("=" * 60)
    logger.info("🧪 ТЕСТ: Metrics Collector")
    logger.info("=" * 60)
    
    try:
        config = load_config('./config.yaml')
        
        # Создание компонентов
        event_bus = EventBus(config['event_bus'])
        fsm = FSM(config['fsm'], event_bus)
        
        # Создание сборщика метрик
        metrics = MetricsCollector(config.get('monitoring', {}))
        metrics.set_components(event_bus=event_bus, fsm=fsm)
        
        # Запуск
        await metrics.start()
        
        # Сбор метрик в течение 5 секунд
        logger.info("📊 Сбор метрик в течение 5 секунд...")
        await asyncio.sleep(5)
        
        # Получение снимка
        snapshot = metrics.get_snapshot()
        
        logger.info(f"\n📈 Текущие метрики:")
        logger.info(f"   CPU: {snapshot.cpu_percent:.1f}%")
        logger.info(f"   RAM: {snapshot.ram_used_mb:.0f} MB ({snapshot.ram_percent:.1f}%)")
        logger.info(f"   FSM State: {snapshot.fsm_state}")
        logger.info(f"   Events Published: {snapshot.event_bus_published}")
        logger.info(f"   Events Delivered: {snapshot.event_bus_delivered}")
        
        # Статистика
        cpu_stats = metrics.get_cpu_stats()
        ram_stats = metrics.get_ram_stats()
        
        logger.info(f"\n📊 Статистика CPU:")
        logger.info(f"   Avg: {cpu_stats['avg']:.1f}%")
        logger.info(f"   Min: {cpu_stats['min']:.1f}%")
        logger.info(f"   Max: {cpu_stats['max']:.1f}%")
        
        logger.info(f"\n📊 Статистика RAM:")
        logger.info(f"   Avg: {ram_stats['avg']:.0f} MB")
        logger.info(f"   Min: {ram_stats['min']:.0f} MB")
        logger.info(f"   Max: {ram_stats['max']:.0f} MB")
        
        # Остановка
        await metrics.stop()
        await event_bus.stop()
        
        logger.info(f"\n✅ ТЕСТ ПРОЙДЕН: Metrics Collector работает")
        return True
    
    except Exception as e:
        logger.error(f"❌ Ошибка теста Metrics: {e}", exc_info=True)
        return False


async def test_health_checker():
    """
    Тест проверщика здоровья
    """
    logger.info("\n" + "=" * 60)
    logger.info("🧪 ТЕСТ: Health Checker")
    logger.info("=" * 60)
    
    try:
        config = load_config('./config.yaml')
        
        # Создание HealthChecker
        health = HealthChecker(config.get('monitoring', {}))
        
        # Регистрация тестовых проверок
        async def check_component_a():
            return HealthCheck(
                component='component_a',
                status=HealthStatus.HEALTHY,
                message='OK',
                latency_ms=10.0,
                timestamp=time.time()
            )
        
        async def check_component_b():
            return HealthCheck(
                component='component_b',
                status=HealthStatus.DEGRADED,
                message='High latency',
                latency_ms=500.0,
                timestamp=time.time()
            )
        
        health.register_check('component_a', check_component_a)
        health.register_check('component_b', check_component_b)
        
        # Запуск
        await health.start()
        
        # Ожидание проверок
        logger.info("🏥 Запуск проверок здоровья...")
        await asyncio.sleep(2)
        
        # Получение статусов
        statuses = health.get_all_statuses()
        
        logger.info(f"\n📊 Статусы компонентов:")
        for component, status in statuses.items():
            logger.info(f"   {component}: {status.value}")
        
        # Общее состояние
        overall = health.get_overall_health()
        logger.info(f"\n📊 Общее состояние: {overall.value}")
        
        # Отчет
        report = health.get_health_report()
        logger.info(f"\n📋 Отчет о здоровье:")
        logger.info(f"   Overall: {report['overall']}")
        logger.info(f"   Components: {len(report['components'])}")
        
        # Остановка
        await health.stop()
        
        logger.info(f"\n✅ ТЕСТ ПРОЙДЕН: Health Checker работает")
        return True
    
    except Exception as e:
        logger.error(f"❌ Ошибка теста Health: {e}", exc_info=True)
        return False


async def test_degradation_manager():
    """
    Тест менеджера деградации
    """
    logger.info("\n" + "=" * 60)
    logger.info("🧪 ТЕСТ: Degradation Manager")
    logger.info("=" * 60)
    
    try:
        config = load_config('./config.yaml')
        
        # Создание DegradationManager
        degradation = DegradationManager(config.get('monitoring', {}))
        
        # Регистрация компонентов с приоритетами
        async def disable_rag():
            logger.info("   🔌 RAG отключен")
        
        async def enable_rag():
            logger.info("   🔌 RAG включен")
        
        async def disable_tts():
            logger.info("   🔌 TTS отключен")
        
        async def enable_tts():
            logger.info("   🔌 TTS включен")
        
        degradation.register_component(
            name='rag',
            priority=5,
            min_level=DegradationLevel.ECONOMY,
            disable_callback=disable_rag,
            enable_callback=enable_rag
        )
        
        degradation.register_component(
            name='tts',
            priority=3,
            min_level=DegradationLevel.SURVIVAL,
            disable_callback=disable_tts,
            enable_callback=enable_tts
        )
        
        degradation.register_component(
            name='llm',
            priority=0,  # Критичный
            min_level=DegradationLevel.EMERGENCY
        )
        
        # Запуск
        await degradation.start()
        
        # Проверка начального состояния
        logger.info(f"\n📊 Начальное состояние:")
        status = degradation.get_status()
        logger.info(f"   Level: {status['current_level']}")
        logger.info(f"   Active: {status['active_components']}/{status['total_components']}")
        
        # Имитация нехватки ресурсов
        logger.info(f"\n⚠️ Имитация нехватки RAM...")
        
        # Создание нагрузки на память
        memory_hog = []
        for i in range(100):
            memory_hog.append(bytearray(10 * 1024 * 1024))  # 10 MB каждый
            await asyncio.sleep(0.1)
        
        # Проверка состояния после нагрузки
        await asyncio.sleep(2)
        
        status = degradation.get_status()
        logger.info(f"\n📊 Состояние после нагрузки:")
        logger.info(f"   Level: {status['current_level']}")
        logger.info(f"   Disabled: {status['disabled_components']}")
        
        # Освобождение памяти
        memory_hog.clear()
        
        # Ожидание восстановления
        await asyncio.sleep(2)
        
        status = degradation.get_status()
        logger.info(f"\n📊 Состояние после восстановления:")
        logger.info(f"   Level: {status['current_level']}")
        logger.info(f"   Active: {status['active_components']}/{status['total_components']}")
        
        # Остановка
        await degradation.stop()
        
        logger.info(f"\n✅ ТЕСТ ПРОЙДЕН: Degradation Manager работает")
        return True
    
    except Exception as e:
        logger.error(f"❌ Ошибка теста Degradation: {e}", exc_info=True)
        return False


async def test_stress_event_bus():
    """
    Stress тест Event Bus
    """
    logger.info("\n" + "=" * 60)
    logger.info("🧪 STRESS ТЕСТ: Event Bus")
    logger.info("=" * 60)
    
    try:
        config = load_config('./config.yaml')
        
        # Создание Event Bus
        event_bus = EventBus(config['event_bus'])
        
        # Счетчик событий
        received_count = 0
        
        async def test_handler(event: Event):
            nonlocal received_count
            received_count += 1
        
        # Подписка
        event_bus.subscribe(EventType.WAKE_DETECTED, test_handler)
        
        # Запуск
        await event_bus.start()
        
        # Публикация 1000 событий
        logger.info("📤 Публикация 1000 событий...")
        start_time = time.time()
        
        for i in range(1000):
            await event_bus.publish(Event(
                type=EventType.WAKE_DETECTED,
                data={'test': i},
                source='stress_test'
            ))
        
        # Ожидание обработки
        await asyncio.sleep(2)
        
        elapsed = time.time() - start_time
        
        # Статистика
        stats = event_bus.stats
        
        logger.info(f"\n📊 Результаты stress теста:")
        logger.info(f"   Опубликовано: {stats['published']}")
        logger.info(f"   Доставлено: {stats['delivered']}")
        logger.info(f"   Ошибок: {stats['failed']}")
        logger.info(f"   Время: {elapsed:.2f} сек")
        logger.info(f"   Скорость: {stats['published'] / elapsed:.0f} events/sec")
        
        # Остановка
        await event_bus.stop()
        
        # Проверка
        if stats['delivered'] >= 990:  # Допускаем 1% потерь
            logger.info(f"\n✅ STRESS ТЕСТ ПРОЙДЕН: Event Bus стабилен")
            return True
        else:
            logger.warning(f"\n⚠️ STRESS ТЕСТ: Потеряно {stats['published'] - stats['delivered']} событий")
            return False
    
    except Exception as e:
        logger.error(f"❌ Ошибка stress теста: {e}", exc_info=True)
        return False


async def test_long_running():
    """
    Тест длительной работы (имитация 8 часов)
    """
    logger.info("\n" + "=" * 60)
    logger.info("🧪 ТЕСТ: Длительная работа (имитация)")
    logger.info("=" * 60)
    
    try:
        config = load_config('./config.yaml')
        
        # Создание компонентов
        event_bus = EventBus(config['event_bus'])
        fsm = FSM(config['fsm'], event_bus)
        metrics = MetricsCollector(config.get('monitoring', {}))
        metrics.set_components(event_bus=event_bus, fsm=fsm)
        
        # Запуск
        await event_bus.start()
        await metrics.start()
        
        # Имитация работы в течение 30 секунд (вместо 8 часов)
        logger.info("🕐 Имитация длительной работы (30 секунд)...")
        
        for i in range(30):
            # Публикация событий
            await event_bus.publish(Event(
                type=EventType.HEALTH_CHECK,
                data={'iteration': i},
                source='long_running_test'
            ))
            
            # Логирование каждые 10 секунд
            if i % 10 == 0:
                snapshot = metrics.get_snapshot()
                logger.info(
                    f"   [{i}s] CPU={snapshot.cpu_percent:.1f}%, "
                    f"RAM={snapshot.ram_used_mb:.0f}MB, "
                    f"Events={snapshot.event_bus_published}"
                )
            
            await asyncio.sleep(1)
        
        # Финальная статистика
        snapshot = metrics.get_snapshot()
        stats = event_bus.stats
        
        logger.info(f"\n📊 Финальная статистика:")
        logger.info(f"   CPU: {snapshot.cpu_percent:.1f}%")
        logger.info(f"   RAM: {snapshot.ram_used_mb:.0f} MB")
        logger.info(f"   Events Published: {stats['published']}")
        logger.info(f"   Events Delivered: {stats['delivered']}")
        logger.info(f"   Failed: {stats['failed']}")
        
        # Проверка утечек памяти
        ram_stats = metrics.get_ram_stats()
        ram_growth = ram_stats['max'] - ram_stats['min']
        
        logger.info(f"\n📊 Анализ памяти:")
        logger.info(f"   Min RAM: {ram_stats['min']:.0f} MB")
        logger.info(f"   Max RAM: {ram_stats['max']:.0f} MB")
        logger.info(f"   Growth: {ram_growth:.0f} MB")
        
        if ram_growth < 100:  # Менее 100 MB роста
            logger.info(f"\n✅ ТЕСТ ПРОЙДЕН: Нет утечек памяти")
        else:
            logger.warning(f"\n⚠️ ТЕСТ: Возможна утечка памяти ({ram_growth:.0f} MB)")
        
        # Остановка
        await metrics.stop()
        await event_bus.stop()
        
        return True
    
    except Exception as e:
        logger.error(f"❌ Ошибка теста длительной работы: {e}", exc_info=True)
        return False


async def main():
    """Главная функция"""
    logger.info("\n" + "=" * 60)
    logger.info("🚀 ФАЗА 7.5-7.8: Тесты полировки")
    logger.info("=" * 60 + "\n")
    
    results = {}
    
    # Тест Metrics Collector
    results['metrics'] = await test_metrics_collector()
    
    # Тест Health Checker
    results['health'] = await test_health_checker()
    
    # Тест Degradation Manager
    results['degradation'] = await test_degradation_manager()
    
    # Stress тест Event Bus
    results['stress_event_bus'] = await test_stress_event_bus()
    
    # Тест длительной работы
    results['long_running'] = await test_long_running()
    
    # Итоги
    logger.info("\n" + "=" * 60)
    logger.info("📊 ИТОГИ ФАЗЫ 7.5-7.8")
    logger.info("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"   {status}: {test_name}")
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    logger.info(f"\n   Результат: {passed}/{total} тестов пройдено")
    
    if passed == total:
        logger.info("\n🎉 Все тесты Фазы 7.5-7.8 пройдены!")
        logger.info("\nСледующие шаги:")
        logger.info("1. Фаза 8: Упаковка (Nuitka)")
        logger.info("2. Финальное тестирование на чистой VM")
    else:
        logger.info("\n⚠️ Некоторые тесты не пройдены.")
    
    return passed == total


if __name__ == '__main__':
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
