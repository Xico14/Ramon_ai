# 🚀 Быстрый старт - Запуск одной командой

## 📋 Требования

Перед запуском убедитесь, что у вас установлены:

- **Python 3.11+** - [Скачать](https://www.python.org/downloads/)
- **Node.js 18+** - [Скачать](https://nodejs.org/)

### Проверка установки:

```bash
python --version   # Должна быть 3.11 или выше
node --version     # Должна быть 18 или выше
```

---

## 🎯 Запуск одной командой

### Windows:
```bash
start.bat
```

### Linux / macOS:
```bash
chmod +x start.sh
./start.sh
```

### Универсальный способ (любая ОС):
```bash
python start.py
```

---

## 🔧 Что делает скрипт запуска

1. ✅ Проверяет наличие Python и Node.js
2. 📦 Устанавливает Python зависимости (FastAPI, Uvicorn)
3. 📦 Устанавливает Node зависимости (React, Tailwind)
4. 🔨 Собирает frontend (npm run build)
5. 🚀 Запускает backend сервер на порту 8000

---

## 🌐 После запуска

Откройте в браузере:

- **Frontend**: http://localhost:8000
- **API**: http://localhost:8000/api
- **Health Check**: http://localhost:8000/api/health
- **WebSocket**: ws://localhost:8000/ws

---

## 📡 API Endpoints

### Основные:
- `GET /api/health` - Проверка здоровья
- `GET /api/metrics` - Системные метрики
- `GET /api/fsm` - Состояние FSM
- `POST /api/chat` - Отправка сообщения
- `GET /api/messages` - История сообщений
- `DELETE /api/messages` - Очистка истории

### Документы:
- `GET /api/documents` - Список документов
- `POST /api/documents` - Загрузка документа
- `DELETE /api/documents/{id}` - Удаление документа

### Инструменты:
- `GET /api/tools` - Список инструментов
- `POST /api/tools/{id}/execute` - Выполнение инструмента

### Логи:
- `GET /api/logs` - Системные логи
- `GET /api/audit` - Аудит-лог

---

## 🛑 Остановка

Нажмите `Ctrl+C` в терминале для остановки сервера.

---

## 🐛 Решение проблем

### Ошибка: "Python не найден"
```bash
# Установите Python 3.11+
# Windows: https://www.python.org/downloads/
# Linux: sudo apt install python3.11
# macOS: brew install python@3.11
```

### Ошибка: "Node.js не найден"
```bash
# Установите Node.js 18+
# https://nodejs.org/
```

### Ошибка: "Port 8000 already in use"
```bash
# Найдите процесс:
# Windows: netstat -ano | findstr :8000
# Linux/Mac: lsof -i :8000

# Завершите процесс или измените порт в server.py
```

### Ошибка: "ModuleNotFoundError: No module named 'fastapi'"
```bash
# Установите зависимости вручную:
pip install -r requirements-backend.txt
```

### Ошибка сборки frontend
```bash
# Очистите кеш и переустановите:
rm -rf node_modules dist
npm install
npm run build
```

---

## 📊 Режим разработки

Если хотите запускать frontend и backend отдельно:

### Терминал 1 - Backend:
```bash
pip install -r requirements-backend.txt
python server.py
```

### Терминал 2 - Frontend (dev mode):
```bash
npm install
npm run dev
```

Frontend будет доступен на http://localhost:5173 с hot-reload.

---

## 🏗️ Ручная сборка

Если скрипт не работает, выполните вручную:

```bash
# 1. Установка Python зависимостей
pip install -r requirements-backend.txt

# 2. Установка Node зависимостей
npm install

# 3. Сборка frontend
npm run build

# 4. Запуск сервера
python server.py
```

---

## 📁 Структура проекта

```
.
├── server.py                 # FastAPI backend
├── start.py                  # Универсальный скрипт запуска
├── start.bat                 # Скрипт для Windows
├── start.sh                  # Скрипт для Linux/Mac
├── requirements-backend.txt  # Python зависимости
├── package.json              # Node зависимости
├── src/                      # Frontend исходники
│   ├── components/
│   ├── pages/
│   ├── hooks/
│   ├── store/
│   └── lib/
├── dist/                     # Собраный frontend (после build)
└── jarvis/                   # Python AI ассистент
```

---

## 🎉 Готово!

После запуска откройте http://localhost:8000 и наслаждайтесь работой Джарвиса!

**Приятного использования! 🤖**
