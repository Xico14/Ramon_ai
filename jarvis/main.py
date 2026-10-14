"""
Джарвис — AI Ассистент
Главная точка входа
"""
import asyncio
import logging
import sys
from pathlib import Path

# СНАЧАЛА создаём все необходимые директории
Path('./logs').mkdir(parents=True, exist_ok=True)
Path('./data').mkdir(parents=True, exist_ok=True)
Path('./models').mkdir(parents=True, exist_ok=True)
Path('./documents').mkdir(parents=True, exist_ok=True)

import yaml
from PyQt6.QtWidgets import QApplication

from core.event_bus import EventBus
from core.fsm import FSM, State
from core.orchestrator import Orchestrator
from core.config import load_config
from ui.main_window import MainWindow

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('./logs/jarvis.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)


async def startup(event_bus, orchestrator):
    """Асинхронный запуск компонентов"""
    try:
        await event_bus.start()
        await orchestrator.start()
        logger.info("🚀 Джарвис запущен!")
    except Exception as e:
        logger.error(f"❌ Ошибка запуска: {e}", exc_info=True)


async def shutdown(event_bus, orchestrator):
    """Асинхронная остановка"""
    try:
        await orchestrator.stop()
        await event_bus.stop()
        logger.info("✅ Джарвис остановлен")
    except Exception as e:
        logger.error(f"❌ Ошибка остановки: {e}", exc_info=True)


def main():
    """Точка входа"""
    logger.info("🤖 Запуск Джарвиса...")
    
    # Загрузка конфигурации
    config = load_config('./config.yaml')
    logger.info("✅ Конфигурация загружена")
    
    # Создание Event Bus
    event_bus = EventBus(config['event_bus'])
    logger.info("✅ Event Bus создан")
    
    # Создание FSM
    fsm = FSM(config['fsm'], event_bus)
    logger.info("✅ FSM создан")
    
    # Создание Orchestrator
    orchestrator = Orchestrator(config, event_bus, fsm)
    logger.info("✅ Orchestrator создан")
    
    # Создание QApplication
    app = QApplication(sys.argv)
    
    # Создание UI
    window = MainWindow(event_bus, fsm)
    window.show()
    logger.info("✅ UI создан")
    
    # Импортируем qasync здесь, после создания QApplication
    from qasync import QEventLoop
    
    # Создание qasync event loop
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    
    logger.info("🔄 Event loop создан (qasync)")
    
    # Обработчик закрытия
    def on_quit():
        logger.info("🛑 Закрытие приложения...")
        # Запускаем shutdown асинхронно
        asyncio.ensure_future(shutdown(event_bus, orchestrator))
    
    app.aboutToQuit.connect(on_quit)
    
    # Запускаем startup как фоновую задачу
    async def run_app():
        """Запуск приложения"""
        # Запуск компонентов
        await startup(event_bus, orchestrator)
    
    # Запускаем в loop
    with loop:
        # Создаём задачу для run_app
        task = loop.create_task(run_app())
        
        # Запускаем Qt event loop (он будет обрабатывать и async задачи)
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            logger.info("🛑 Остановка по Ctrl+C")
        finally:
            # Отмена задачи
            if not task.done():
                task.cancel()
                try:
                    loop.run_until_complete(task)
                except asyncio.CancelledError:
                    pass


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}", exc_info=True)
        sys.exit(1)
