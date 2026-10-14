# 🐛 Исправление проблемы с Event Loop

## Проблема

При запуске `python main.py` возникала ошибка:

```
RuntimeError: Cannot enter into task <Task pending name='Task-2' coro=<EventBus.publish()>> 
while another task <Task pending name='Task-1' coro=<main()>> is being executed.
```

## Причина

Конфликт между двумя event loop:
1. **asyncio event loop** — для асинхронных задач Python
2. **Qt event loop** — для графического интерфейса PyQt6

Когда `EventBus` создавался, он инициализировал `asyncio.Queue()` до того, как был установлен правильный event loop через `qasync`. Это приводило к тому, что queue был привязан к одному loop, а использовался в другом.

## Решение

### 1. Ленивая инициализация Queue

**Файл:** `jarvis/core/event_bus.py`

```python
# БЫЛО: Queue создавался в __init__
def __init__(self, config: dict):
    self._queue: asyncio.Queue = asyncio.Queue(maxsize=self.max_queue_size)

# СТАЛО: Queue создаётся при первом использовании
def __init__(self, config: dict):
    self._queue: asyncio.Queue | None = None

async def publish(self, event: Event) -> None:
    if self._queue is None:
        self._queue = asyncio.Queue(maxsize=self.max_queue_size)
    # ...
```

### 2. Правильная интеграция qasync

**Файл:** `jarvis/main.py`

```python
# Создание QApplication ПЕРЕД asyncio
app = QApplication(sys.argv)

# Создание qasync event loop
from qasync import QEventLoop
loop = QEventLoop(app)
asyncio.set_event_loop(loop)

# Запуск startup как фоновой задачи (не блокирует Qt loop)
async def run_app():
    await startup(event_bus, orchestrator)

with loop:
    task = loop.create_task(run_app())
    loop.run_forever()  # Qt loop обрабатывает и async задачи
```

### 3. Разделение startup и shutdown

```python
async def startup(event_bus, orchestrator):
    """Асинхронный запуск компонентов"""
    await event_bus.start()
    await orchestrator.start()

async def shutdown(event_bus, orchestrator):
    """Асинхронная остановка"""
    await orchestrator.stop()
    await event_bus.stop()
```

## Ключевые моменты

### ✅ Правильно:

1. **Создавать QApplication первым** — до любого asyncio кода
2. **Использовать qasync.QEventLoop** — для интеграции Qt и asyncio
3. **Ленивая инициализация** — asyncio объекты создаются внутри event loop
4. **Фоновые задачи** — `loop.create_task()` вместо блокирующих вызовов

### ❌ Неправильно:

1. **asyncio.run()** — создаёт свой event loop, конфликтует с Qt
2. **Создание asyncio.Queue в __init__** — до установки event loop
3. **Блокирующие вызовы** — `loop.run_until_complete()` в main loop
4. **Два event loop** — asyncio и Qt должны быть интегрированы через qasync

## Тестирование

### Тест EventBus без Qt

```bash
python scripts/test_event_bus.py
```

Этот тест проверяет работу EventBus в чистом asyncio, без Qt.

### Тест с Qt

```bash
python main.py
```

Теперь должно работать без ошибок event loop.

## Альтернативные решения

### Вариант 1: Использовать только asyncio (без Qt)

Если не нужен графический интерфейс:

```python
async def main():
    # ... создание компонентов ...
    await event_bus.start()
    await orchestrator.start()
    
    # Держим приложение запущенным
    while True:
        await asyncio.sleep(1)

asyncio.run(main())
```

### Вариант 2: Использовать только Qt (без asyncio)

Если не нужна асинхронность:

```python
app = QApplication(sys.argv)
window = MainWindow()
window.show()

# Синхронный код
event_bus = EventBus(config)
# ...

sys.exit(app.exec())
```

### Вариант 3: qasync (текущее решение)

Интеграция Qt и asyncio через qasync — **рекомендуется**.

## Полезные ссылки

- [qasync документация](https://github.com/CabbageDevelopment/qasync)
- [PyQt6 и asyncio](https://doc.qt.io/qtforpython-6/PySide6/QtCore/QEventLoop.html)
- [Python asyncio best practices](https://docs.python.org/3/library/asyncio-dev.html)

## Проверка

После исправления запустите:

```bash
# 1. Тест EventBus
python scripts/test_event_bus.py

# 2. Запуск Джарвиса
python main.py
```

Оба должны работать без ошибок event loop. ✅
