# 🛠️ Инструкция по установке Джарвиса (Windows)

## ⚡ Быстрая установка (рекомендуется)

```bash
# Перейдите в папку проекта
cd jarvis

# Запустите скрипт автоматической установки
python scripts/install.py
```

Скрипт установит все зависимости поэтапно и покажет результат.

---

## 📋 Ручная установка (пошагово)

### Шаг 1: Проверьте Python

```bash
python --version
```

Должна быть версия **3.11** или новее (3.12, 3.13).

### Шаг 2: Обновите pip

```bash
python -m pip install --upgrade pip setuptools wheel
```

### Шаг 3: Установите базовые зависимости

```bash
pip install -r requirements-minimal.txt
```

Это установит:
- pydantic, pyyaml, psutil
- aiosqlite (база данных)
- numpy (работа с аудио)
- PyQt6, qasync (интерфейс)

### Шаг 4: Установите PyAudio

**Вариант A: Автоматически**
```bash
pip install pyaudio
```

**Вариант B: Если возникла ошибка (Windows)**

1. Скачайте Visual C++ Build Tools:
   - https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Установите с опцией "Разработка классических приложений на C++"

2. Или скачайте pre-compiled wheel:
   - Перейдите: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
   - Скачайте файл для вашей версии Python (например, `PyAudio-0.2.14-cp313-cp313-win_amd64.whl`)
   - Установите: `pip install PyAudio-0.2.14-cp313-cp313-win_amd64.whl`

### Шаг 5: Установите LLM

```bash
pip install llama-cpp-python
```

⚠️ **Важно:** Компиляция может занять 5-10 минут.

**Для GPU (NVIDIA CUDA):**
```bash
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121
```

### Шаг 6: Установите STT (распознавание речи)

```bash
pip install faster-whisper
```

### Шаг 7: Установите Wake Word (опционально)

```bash
pip install openwakeword
```

### Шаг 8: Установите RAG (опционально, тяжело)

```bash
pip install sentence-transformers rank-bm25
```

⚠️ **Внимание:** sentence-transformers скачает модели (~2 GB).

---

## 🧪 Проверка установки

```bash
# Запустите тесты Фазы 0
python scripts/test_phase0.py
```

Должно вывести:
```
🚀 ФАЗА 0: Proof of Concept
...
✅ P0 Tool-calling: ...
✅ P0 Wake Word: ...
✅ P1 STT: ...
✅ P2 RAM: ...
```

---

## 📥 Скачивание моделей

### LLM (обязательно)

```bash
# Создайте папку для моделей
mkdir models

# Скачайте Qwen2.5-3B (2 GB)
curl -L -o models/qwen2.5-3b-q4_k_m.gguf https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF/resolve/main/qwen2.5-3b-instruct-q4_k_m.gguf
```

**Или через браузер:**
1. Перейдите: https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF
2. Скачайте файл `qwen2.5-3b-instruct-q4_k_m.gguf`
3. Поместите в папку `jarvis/models/`

### Whisper (автоматически)

Модель Whisper скачается автоматически при первом запуске (~1.5 GB).

---

## 🚀 Запуск Джарвиса

```bash
python main.py
```

Должно открыться окно с интерфейсом Джарвиса.

---

## ❓ Решение проблем

### Ошибка: "ModuleNotFoundError: No module named 'pyaudio'"

**Решение:**
```bash
# Windows
pip install pipwin
pipwin install pyaudio

# Или используйте pre-compiled wheel (см. Шаг 4)
```

### Ошибка: "Could not find a version that satisfies the requirement faiss-cpu"

**Решение:**
```bash
# Установите последнюю версию
pip install faiss-cpu

# Или пропустите (RAG не будет работать)
# Используйте requirements-minimal.txt вместо requirements.txt
```

### Ошибка: "llama-cpp-python не компилируется"

**Решение:**
1. Установите Visual C++ Build Tools
2. Или используйте pre-compiled wheel:
```bash
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
```

### Ошибка: "CUDA out of memory"

**Решение:**
- Используйте CPU версию (без GPU)
- Или уменьшите размер модели (Qwen2.5-1B вместо 3B)

### Ошибка: "PyQt6 не запускается"

**Решение:**
```bash
# Переустановите PyQt6
pip uninstall PyQt6
pip install PyQt6
```

---

## 📊 Требования к системе

### Минимальные:
- **ОС:** Windows 10/11 (64-bit)
- **Python:** 3.11+
- **RAM:** 8 GB
- **Диск:** 10 GB свободного места
- **CPU:** 4+ ядра

### Рекомендуемые:
- **RAM:** 16 GB
- **GPU:** NVIDIA с CUDA (для ускорения LLM)
- **Диск:** SSD

---

## 🎯 Что дальше?

После успешной установки:

1. **Запустите тесты:**
   ```bash
   python scripts/test_phase0.py
   ```

2. **Запустите Джарвиса:**
   ```bash
   python main.py
   ```

3. **Скажите "Джарвис" для активации** (если настроен Wake Word)

---

## 📞 Нужна помощь?

Если возникли проблемы:
1. Проверьте версию Python: `python --version`
2. Проверьте список установленных пакетов: `pip list`
3. Запустите тесты: `python scripts/test_phase0.py`
4. Проверьте логи в папке `logs/`

---

**Удачи в использовании Джарвиса! 🤖**
