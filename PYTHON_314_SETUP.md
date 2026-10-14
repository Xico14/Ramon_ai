# 🐍 Установка для Python 3.14

## Проблема

Python 3.14 - очень новая версия, и некоторые старые пакеты не имеют pre-compiled wheel для неё.

## Решение

### Вариант 1: Автоматическая установка (рекомендуется)

```bash
# Обновите pip до последней версии
python -m pip install --upgrade pip setuptools wheel

# Установите зависимости с флагом --upgrade
pip install --upgrade -r requirements-backend.txt
```

### Вариант 2: Ручная установка пакетов

Если автоматическая установка не работает, установите пакеты по одному:

```bash
# 1. Обновите базовые инструменты
python -m pip install --upgrade pip setuptools wheel

# 2. Установите pydantic (самая новая версия)
pip install --upgrade pydantic

# 3. Установите FastAPI
pip install --upgrade fastapi

# 4. Установите Uvicorn
pip install --upgrade "uvicorn[standard]"

# 5. Установите остальные пакеты
pip install --upgrade websockets python-multipart
```

### Вариант 3: Использование pre-release версий

Если стабильные версии не работают:

```bash
pip install --pre --upgrade pydantic fastapi uvicorn
```

### Вариант 4: Откат на Python 3.12 (если ничего не помогает)

Python 3.12 - стабильная версия с полной поддержкой всех пакетов:

1. Скачайте Python 3.12: https://www.python.org/downloads/release/python-3128/
2. Установите его
3. Используйте `python3.12` вместо `python`

## Проверка установки

После установки проверьте:

```bash
python -c "import fastapi; print(f'FastAPI {fastapi.__version__}')"
python -c "import pydantic; print(f'Pydantic {pydantic.__version__}')"
python -c "import uvicorn; print(f'Uvicorn {uvicorn.__version__}')"
```

Должно вывести версии без ошибок.

## Запуск сервера

После успешной установки зависимостей:

```bash
python server.py
```

Сервер запустится на http://localhost:8000

## Если возникли ошибки

### Ошибка: "No matching distribution found"

Это значит, что для вашей версии Python нет pre-compiled wheel. Решение:

```bash
# Установите Rust компилятор (требуется для сборки)
# Windows: https://rustup.rs/
# Linux: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
# macOS: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Затем попробуйте установить снова
pip install --upgrade pydantic
```

### Ошибка: "Microsoft Visual C++ 14.0 or greater is required"

Установите Visual C++ Build Tools:
https://visualstudio.microsoft.com/visual-cpp-build-tools/

### Ошибка: "Rust compiler not found"

Установите Rust:
- Windows: https://rustup.rs/
- Linux/macOS: `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`

## Альтернатива: Docker

Если ничего не помогает, используйте Docker:

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements-backend.txt .
RUN pip install --no-cache-dir -r requirements-backend.txt

COPY . .
EXPOSE 8000
CMD ["python", "server.py"]
```

Запуск:
```bash
docker build -t jarvis-ai .
docker run -p 8000:8000 jarvis-ai
```

## Поддержка

Если проблема не решена:
1. Проверьте версию Python: `python --version`
2. Проверьте версию pip: `pip --version`
3. Попробуйте создать виртуальное окружение:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/macOS
   pip install --upgrade -r requirements-backend.txt
   ```

## Успешная установка

После успешной установки вы увидите:

```
✅ FastAPI установлен
✅ Pydantic установлен
✅ Uvicorn установлен
```

Теперь можно запускать:
```bash
python start.py
```
