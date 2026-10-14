# 🤖 Джарвис AI - Полноценный AI Ассистент

Современный AI-ассистент с голосовым управлением, работающий локально на вашем компьютере.

## 🌟 Возможности

### 🎤 Голосовое управление
- Распознавание речи (STT)
- Синтез речи (TTS)
- Wake word активация
- Barge-in (перебивание)

### 🧠 AI ядро
- Локальная LLM (Qwen2.5-3B)
- Контекстная память
- Tool calling
- RAG (поиск в документах)

### 🎨 Современный интерфейс
- React + TypeScript
- Адаптивный дизайн
- Real-time метрики
- WebSocket обновления

### 🔐 Безопасность
- Шифрование данных
- Контроль доступа
- Аудит-лог
- Изолированное выполнение

---

## 🚀 Быстрый старт

### Одна команда для запуска:

**Windows:**
```bash
start.bat
```

**Linux / macOS:**
```bash
chmod +x start.sh
./start.sh
```

**Универсально:**
```bash
python start.py
```

После запуска откройте: **http://localhost:8000**

---

## 📋 Требования

- **Python 3.11+**
- **Node.js 18+**
- **RAM:** минимум 8 GB (рекомендуется 16 GB)
- **Диск:** 10 GB свободного места

---

## 🏗️ Архитектура

```
┌─────────────────────────────────────────────┐
│         Frontend (React + TypeScript)       │
│  ┌───────────────────────────────────────┐  │
│  │  Dashboard │ Chat │ Docs │ Tools      │  │
│  └───────────────────────────────────────┘  │
└─────────────────┬───────────────────────────┘
                  │ HTTP/WebSocket
┌─────────────────▼───────────────────────────┐
│      Backend (FastAPI + Python)             │
│  ┌───────────────────────────────────────┐  │
│  │  API │ WebSocket │ Static Files       │  │
│  └───────────────────────────────────────┘  │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│         AI Core (jarvis/)                   │
│  ┌───────────────────────────────────────┐  │
│  │  LLM │ STT │ TTS │ RAG │ FSM         │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

---

## 📁 Структура проекта

```
jarvis-ai/
├── server.py                 # FastAPI backend
├── start.py                  # Скрипт запуска
├── start.bat                 # Windows скрипт
├── start.sh                  # Linux/Mac скрипт
├── requirements-backend.txt  # Python зависимости
├── package.json              # Node зависимости
│
├── src/                      # Frontend
│   ├── components/
│   │   └── layout/
│   │       ├── Layout.tsx
│   │       ├── Sidebar.tsx
│   │       └── Header.tsx
│   ├── pages/
│   │   ├── DashboardPage.tsx
│   │   ├── ChatPage.tsx
│   │   ├── DocumentsPage.tsx
│   │   ├── ToolsPage.tsx
│   │   ├── SettingsPage.tsx
│   │   ├── LogsPage.tsx
│   │   └── SecurityPage.tsx
│   ├── hooks/
│   │   ├── useChat.ts
│   │   ├── useVoice.ts
│   │   └── useMetrics.ts
│   ├── store/
│   │   └── index.ts
│   ├── types/
│   │   └── index.ts
│   └── lib/
│       ├── api.ts
│       └── utils.ts
│
├── jarvis/                   # AI Core
│   ├── main.py              # Точка входа
│   ├── config.yaml          # Конфигурация
│   ├── core/                # Ядро системы
│   │   ├── event_bus.py
│   │   ├── fsm.py
│   │   └── orchestrator.py
│   ├── brain/               # LLM
│   │   └── llm.py
│   ├── audio/               # Аудио подсистема
│   │   ├── capture.py
│   │   ├── vad.py
│   │   ├── stt.py
│   │   ├── tts.py
│   │   ├── aec.py
│   │   └── wake_word.py
│   ├── rag/                 # RAG система
│   │   ├── ingestion.py
│   │   ├── chunker.py
│   │   ├── embedder.py
│   │   └── search.py
│   ├── security/            # Безопасность
│   │   ├── mcp.py
│   │   ├── scopes.py
│   │   ├── encryption.py
│   │   └── backup.py
│   ├── monitoring/          # Мониторинг
│   │   ├── metrics.py
│   │   ├── health.py
│   │   └── degradation.py
│   └── scripts/             # Скрипты
│       ├── test_phase0.py
│       ├── test_phase45.py
│       ├── test_phase6.py
│       ├── test_phase7.py
│       └── test_phase75.py
│
└── dist/                    # Собраный frontend
```

---

## 🎯 Фазы разработки

### ✅ Завершенные фазы:

- **Фаза 0**: Proof of Concept
- **Фаза 1**: Фундамент (LLM)
- **Фаза 2**: Тело и Нервы (Event Bus, FSM)
- **Фаза 3**: Слух (STT)
- **Фаза 4**: Голос (TTS)
- **Фаза 4.5**: Рефлексы (AEC, Barge-in)
- **Фаза 5**: Пробуждение (Wake Word)
- **Фаза 6**: Память (RAG)
- **Фаза 7**: Безопасность (MCP, Scopes)
- **Фаза 7.5**: Полировка (Monitoring)

### 📊 Статистика:
- **Файлов:** 50+
- **Строк кода:** 10,000+
- **Компонентов:** 15+
- **Тестов:** 20+

---

## 🔌 API Документация

### Основные endpoints:

```bash
# Health check
GET /api/health

# Системные метрики
GET /api/metrics

# Состояние FSM
GET /api/fsm

# Чат
POST /api/chat
Body: { "message": "Привет!" }

# История сообщений
GET /api/messages
DELETE /api/messages

# Документы
GET /api/documents
POST /api/documents
DELETE /api/documents/{id}

# Инструменты
GET /api/tools
POST /api/tools/{id}/execute

# Логи
GET /api/logs
GET /api/audit
```

### WebSocket:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Real-time update:', data);
};
```

---

## 🎨 Frontend страницы

### 📊 Dashboard
- Системные метрики в реальном времени
- Статистика использования
- Быстрые действия

### 💬 Chat
- Голосовой ввод/вывод
- История диалога
- Визуализация состояний FSM

### 📄 Documents
- Загрузка документов (PDF, TXT, MD, DOCX)
- Поиск по документам
- Управление коллекцией

### 🛠️ Tools
- 8 встроенных инструментов
- Контроль доступа
- Уровни риска

### 🔐 Security
- Аудит-лог
- Статистика безопасности
- Контроль высокого риска

### ⚙️ Settings
- Голосовые настройки
- Параметры LLM
- Настройки RAG
- Безопасность

### 📜 Logs
- Системные события
- Отладочная информация
- Фильтрация по уровню

---

## 🧪 Тестирование

```bash
# Тесты Фазы 0
python jarvis/scripts/test_phase0.py

# Тесты Фазы 4.5
python jarvis/scripts/test_phase45.py

# Тесты Фазы 6
python jarvis/scripts/test_phase6.py

# Тесты Фазы 7
python jarvis/scripts/test_phase7.py

# Тесты Фазы 7.5
python jarvis/scripts/test_phase75.py
```

---

## 📚 Документация

- [QUICKSTART.md](QUICKSTART.md) - Быстрый старт
- [FRONTEND_README.md](FRONTEND_README.md) - Frontend документация
- [jarvis/README.md](jarvis/README.md) - AI Core документация
- [jarvis/docs/](jarvis/docs/) - Документация по фазам

---

## 🛠️ Разработка

### Режим разработки:

**Backend:**
```bash
python server.py
```

**Frontend (с hot-reload):**
```bash
npm run dev
```

### Сборка production:

```bash
npm run build
python server.py
```

---

## 📊 Метрики производительности

| Метрика | Цель | Статус |
|---------|------|--------|
| Ear-to-mouth latency | < 2.5 сек | ✅ |
| WER (распознавание) | < 10% | ✅ |
| RAG Recall@5 | > 80% | ✅ |
| RAM потребление | < 8 GB | ✅ |
| Event Bus throughput | > 500/sec | ✅ |

---

## 🔐 Безопасность

- ✅ AES-GCM шифрование
- ✅ Контроль доступа (Scopes)
- ✅ Аудит-лог всех действий
- ✅ Подтверждение опасных операций
- ✅ Изолированное выполнение инструментов
- ✅ Резервное копирование

---

## 🤝 Вклад

Проект открыт для вклада! Если хотите помочь:

1. Fork репозитория
2. Создайте ветку для фичи
3. Сделайте commit
4. Откройте Pull Request

---

## 📝 Лицензия

MIT License

---

## 🎉 Благодарности

- **Qwen** - за LLM модель
- **Silero** - за VAD и TTS
- **Whisper** - за STT
- **FastAPI** - за backend фреймворк
- **React** - за frontend фреймворк

---

## 📞 Поддержка

Если возникли проблемы:

1. Проверьте [QUICKSTART.md](QUICKSTART.md)
2. Посмотрите логи в `logs/`
3. Проверьте [документацию](jarvis/docs/)

---

**Создано с ❤️ для AI-ассистентов нового поколения**

🤖 **Джарвис AI v1.0**
