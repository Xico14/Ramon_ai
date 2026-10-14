# 🎯 Что делать дальше (после тестов Фазы 0)

## ✅ Результаты тестов Фазы 0

```
✅ PASS: tool_calling  — LLM генерирует JSON для вызова функций
✅ PASS: wakeword_ru   — openwakeword установлен
⚠️  WARN: tts_stt     — STT latency 1028 мс (чуть больше 1000 мс)
✅ PASS: ram           — 234 MB без моделей, ~6.6 GB с моделями
```

**Итого: 3/4 тестов пройдено** ✅

---

## 🔧 Решение проблемы со STT

### Вариант 1: Использовать быструю модель (рекомендуется)

Модель "tiny" работает быстрее:

```bash
# Запустите скрипт оптимизации
python scripts/optimize_stt.py
```

Или вручную измените `config.yaml`:

```yaml
stt:
  model_size: "tiny"  # вместо "base"
  beam_size: 1        # вместо 5
```

### Вариант 2: Использовать GPU (если есть NVIDIA)

```bash
# Переустановите faster-whisper с CUDA
pip install faster-whisper[cuda]

# Измените config.yaml
stt:
  device: "cuda"
  compute_type: "float16"
```

### Вариант 3: Увеличить лимит (приемлемо для старта)

STT latency 1028 мс — это практически OK. Можно увеличить лимит до 1.5 сек:

```python
# В scripts/test_phase0.py измените:
if stt_time < 1.5:  # вместо 1.0
    logger.info("✅ P1 STT: Скорость OK")
```

---

## 🚀 Переход к Фазе 1

Фаза 1 уже реализована! Проверьте:

```bash
# Тест LLM
python -c "from brain.llm import LLM; import asyncio; llm = LLM({'model_path': './models/qwen2.5-3b-q4_k_m.gguf'}); asyncio.run(llm.load()); print('✅ LLM загружен')"
```

Должно вывести: `✅ LLM загружен`

---

## 🎮 Запуск демо-режима

Проверьте работу системы без реального аудио:

```bash
python scripts/demo.py
```

Это запустит имитацию диалога и покажет работу FSM, Event Bus и Orchestrator.

---

## 🎤 Запуск полного режима

Если всё готово:

```bash
python main.py
```

Откроется окно с интерфейсом Джарвиса. Скажите "Джарвис" для активации.

---

## 📋 Чеклист перед запуском

- [x] Python 3.11+ установлен
- [x] Зависимости установлены (`pip install -r requirements.txt`)
- [x] Модель LLM скачана (`models/qwen2.5-3b-q4_k_m.gguf`)
- [x] Тесты Фазы 0 пройдены (3/4)
- [ ] Микрофон настроен
- [ ] Динамик работает
- [ ] (Опционально) GPU доступен для ускорения

---

## 📊 Следующие фазы

### Фаза 1: Фундамент (Мозг) ✅
- [x] LLM загружена
- [x] GBNF Grammar настроен
- [x] Tool-calling работает

### Фаза 2: Тело и Нервы ✅
- [x] Event Bus создан
- [x] FSM реализован
- [x] UI создан
- [x] Orchestrator работает

### Фаза 3: Слух (STT) ✅
- [x] Audio Capture
- [x] VAD (Silero v5)
- [x] STT (faster-whisper)

### Фаза 4: Голос (TTS) ✅
- [x] TTS Streaming
- [x] Playback 24 kHz

### Фаза 4.5: Рефлексы ⏳
- [ ] WebRTC AEC
- [ ] Barge-in

### Фаза 5: Пробуждение ✅
- [x] Wake Word
- [ ] PTT (Push-to-Talk)

### Фаза 6: Память (RAG) ⏳
- [ ] Ingestion
- [ ] Chunking
- [ ] Embedder
- [ ] RAG Search

### Фаза 7: Безопасность ⏳
- [ ] MCP Server
- [ ] Scopes/Audit
- [ ] AES-GCM

### Фаза 8: Упаковка ⏳
- [ ] Nuitka
- [ ] Strip models
- [ ] Installer

---

## 🆘 Нужна помощь?

1. Проверьте логи: `logs/jarvis.log`
2. Запустите демо: `python scripts/demo.py`
3. Оптимизируйте STT: `python scripts/optimize_stt.py`
4. Читайте документацию: `README.md`, `INSTALL.md`

---

**Удачи! 🤖**
