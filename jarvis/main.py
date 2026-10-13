"""
Джарвис — AI Ассистент
Главная точка входа
"""
import asyncio
import logging
import sys
from pathlib import Path

import yaml
from qasync import QEventLoop
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


async def main():
    """Главная асинхронная функция"""
    logger.info("🤖 Запуск Джарвиса...")
    
    # Загрузка конфигурации
    config = load_config('./config.yaml')
    logger.info(f"✅ Конфигурация загружена")
    
    # Создание Event Bus
    event_bus = EventBus(config['event_bus'])
    logger.info("✅ Event Bus создан")
    
    # Создание FSM
    fsm = FSM(config['fsm'], event_bus)
    logger.info("✅ FSM создан")
    
    # Создание Orchestrator
    orchestrator = Orchestrator(config, event_bus, fsm)
    logger.info("✅ Orchestrator создан")
    
    # Создание UI
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    
    window = MainWindow(event_bus, fsm)
    window.show()
    logger.info("✅ UI создан")
    
    # Запуск всех компонентов
    try:
        await orchestrator.start()
        logger.info("🚀 Джарвис запущен!")
        
        # Запуск event loop
        with loop:
            loop.run_forever()
    except KeyboardInterrupt:
        logger.info("🛑 Остановка по Ctrl+C")
    finally:
        await orchestrator.stop()
        logger.info("✅ Джарвис остановлен")


if __name__ == '__main__':
    # Создание необходимых директорий
    Path('./logs').mkdir(exist_ok=True)
    Path('./data').mkdir(exist_ok=True)
    Path('./models').mkdir(exist_ok=True)
    Path('./documents').mkdir(exist_ok=True)
    
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}", exc_info=True)
        sys.exit(1)
