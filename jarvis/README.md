# 🤖 Джарвис — AI Ассистент

Голосовой AI-ассистент, который живёт в компьютере. Слушает, говорит, читает книги и управляет программами.

## 🏗️ Архитектура

```
┌─────────────────────────────────────────────────────────────┐
│                    EVENT BUS (asyncio)                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  🎤 Микрофон → 👂 VAD → 📝 STT → 🧠 LLM → 🔊 TTS → 🔈 Динамик │
│                                                              │
│  ⏰ Wake Word ──────────────────────────────────────────────│
│                                                              │
│  📚 RAG ←→ 🧠 LLM                                           │
│                                                              │
│  🔄 FSM: IDLE → WAKE → LISTEN → THINK → SPEAK → BARGE_IN   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
cd jarvis
pip install -r requirements.txt
```

### 2. Скачивание моделей

```bash
# LLM (Qwen2.5-3B Q4_K_M)
mkdir -p models
wget https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF/resolve/main/qwen2.5-3b-instruct-q4_k_m.gguf -O models/qwen2.5-3b-q4_k_m.gguf

# Whisper (автоматически при первом запуске)
# Silero VAD (автоматически при первом запуске)
```

### 3. Запуск тестов Фазы 0

```bash
python scripts/test_phase0.py
```

### 4. Запуск Джарвиса

```bash
python main.py
```

## 📋 Дорожная карта

### 🟢 Фаза 0: Proof of Concept
- [x] P0: Tool-calling
- [x] P0: Wake Word RU
- [x] P1: TTS/STT скорость
- [x] P2: RAM потребление

### 🔵 Фаза 1: Фундамент (Мозг)
- [x] Установка llama-cpp-python
- [x] Загрузка Qwen2.5-3B Q4
- [x] Настройка GBNF Grammar

### 🔵 Фаза 2: Тело и Нервы
- [x] Event Bus + DLQ
- [x] FSM (IDLE → WAKE → LISTEN → THINK → SPEAK)
- [x] UI на PyQt6
- [x] ContextBuilder

### 🔵 Фаза 3: Слух (STT)
- [x] Audio Capture (16 kHz)
- [x] VAD (Silero v5)
- [x] STT (faster-whisper)

### 🔵 Фаза 4: Голос (TTS)
- [x] TTS Streaming
- [x] Playback 24 kHz

### 🔵 Фаза 4.5: Рефлексы
- [ ] WebRTC AEC
- [ ] Barge-in

### 🔵 Фаза 5: Пробуждение
- [ ] Wake Word (openwakeword)
- [ ] PTT (Push-to-Talk)

### 🔵 Фаза 6: Память (RAG)
- [ ] Ingestion (PDF/OCR)
- [ ] Chunking
- [ ] Embedder
- [ ] RAG (BM25 + vector)

### 🔵 Фаза 7: Безопасность
- [ ] MCP Server
- [ ] Scopes/Audit
- [ ] AES-GCM шифрование

### 🟡 Фаза 7.5: Полировка
- [ ] Beta тестирование
- [ ] Performance тест
- [ ] Degradation mode

### 🟢 Фаза 8: Упаковка
- [ ] Nuitka компиляция
- [ ] Strip models
- [ ] Clean VM тест

## 📊 Метрики

| Метрика | Цель | Текущее |
|---------|------|---------|
| Ear-to-mouth latency | < 2.5 сек | — |
| WER (распознавание) | < 10% | — |
| RAG Recall@5 | > 80% | — |
| RAM пик | < 8 GB | — |
| Wake Word FAR | < 1/час | — |

## 🛠️ Технологический стек

- **Python 3.11+** — основной язык
- **asyncio** — асинхронность
- **llama-cpp-python** — LLM (Qwen2.5-3B)
- **faster-whisper** — STT
- **Silero VAD** — детектор речи
- **PyQt6** — UI
- **SQLite** — база данных
- **WebRTC** — AEC (подавление эхо)
- **FAISS** — векторный поиск
- **Nuitka** — компиляция

## 📁 Структура проекта

```
jarvis/
├── main.py                 # Точка входа
├── config.yaml             # Конфигурация
├── requirements.txt        # Зависимости
├── core/                   # Ядро системы
│   ├── event_bus.py        # Шина событий
│   ├── fsm.py              # Конечный автомат
│   ├── orchestrator.py     # Оркестратор
│   └── config.py           # Конфигурация
├── brain/                  # Мозг
│   └── llm.py              # LLM (Qwen2.5-3B)
├── audio/                  # Аудио подсистема
│   ├── capture.py          # Захват звука
│   ├── vad.py              # Детектор речи
│   ├── stt.py              # Распознавание
│   ├── tts.py              # Синтез речи
│   └── wake_word.py        # Wake word
├── ui/                     # Интерфейс
│   └── main_window.py      # Главное окно
├── scripts/                # Скрипты
│   └── test_phase0.py      # Тесты Фазы 0
├── models/                 # Модели нейросетей
├── data/                   # Данные (БД, DLQ)
├── documents/              # Документы для RAG
└── logs/                   # Логи
```

## 🔐 Безопасность

- **Scopes** — система разрешений для инструментов
- **AES-GCM** — шифрование настроек
- **Audit Log** — логирование всех действий
- **Confirmation** — запрос подтверждения для опасных операций

## 📝 Лицензия

MIT

## 🤝 Contributing

1. Fork репозитория
2. Создайте ветку для фичи
3. Сделайте commit
4. Откройте Pull Request

---

**Создано с ❤️ для голосовых AI-ассистентов**
