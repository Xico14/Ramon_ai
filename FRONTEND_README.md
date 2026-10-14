# 🤖 Джарвис AI - Frontend

Современный веб-интерфейс для AI-ассистента Джарвис.

## 🚀 Возможности

### 📊 Дашборд
- Обзор системы в реальном времени
- Статистика сообщений, документов, инструментов
- Системные метрики (CPU, RAM, события)
- Быстрые действия

### 💬 Чат
- Диалог с AI-ассистентом
- Голосовой ввод (Web Speech API)
- Синтез речи (Speech Synthesis API)
- Визуализация голосовых волн
- Индикатор состояния FSM

### 📄 Документы (RAG)
- Загрузка документов (PDF, TXT, MD, DOCX)
- Поиск по документам
- Управление коллекцией
- Статистика чанков

### 🛠️ Инструменты (MCP)
- Управление инструментами
- Контроль доступа (scopes)
- Уровни риска (low/medium/high)
- Подтверждение опасных операций

### 🔐 Безопасность
- Аудит-лог всех действий
- Статистика успешных/неудачных операций
- Контроль высокого риска
- Мониторинг безопасности

### ⚙️ Настройки
- Общие настройки (язык, wake word)
- Голосовые настройки (скорость, высота)
- Параметры LLM (temperature, max tokens)
- Настройки RAG (top K, chunk size)

### 📜 Логи
- Системные события
- Отладочная информация
- Фильтрация по уровню
- Очистка логов

## 🎨 Технологии

- **React 18** - UI библиотека
- **TypeScript** - типизация
- **Tailwind CSS** - стилизация
- **Framer Motion** - анимации
- **React Router** - роутинг
- **Zustand** - управление состоянием
- **Lucide React** - иконки
- **Vite** - сборщик

## 📦 Установка

```bash
npm install
```

## 🏃 Запуск

### Режим разработки
```bash
npm run dev
```
Откроется на http://localhost:5173

### Production сборка
```bash
npm run build
npm run preview
```

## 🏗️ Структура проекта

```
src/
├── components/
│   └── layout/
│       ├── Layout.tsx      # Основной layout
│       ├── Sidebar.tsx     # Боковая панель
│       └── Header.tsx      # Верхняя панель
├── pages/
│   ├── DashboardPage.tsx   # Дашборд
│   ├── ChatPage.tsx        # Чат
│   ├── DocumentsPage.tsx   # Документы
│   ├── ToolsPage.tsx       # Инструменты
│   ├── SettingsPage.tsx    # Настройки
│   ├── LogsPage.tsx        # Логи
│   └── SecurityPage.tsx    # Безопасность
├── hooks/
│   ├── useVoice.ts         # Голосовой ввод/вывод
│   └── useChat.ts          # Логика чата
├── store/
│   └── index.ts            # Zustand store
├── types/
│   └── index.ts            # TypeScript типы
├── lib/
│   └── utils.ts            # Утилиты
└── App.tsx                 # Главный компонент
```

## 🔌 Интеграция с бэкендом

Frontend готов к интеграции с Python бэкендом через:

### REST API
```typescript
// Пример API клиента
const API_BASE = 'http://localhost:8000';

async function sendMessage(message: string) {
  const response = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message })
  });
  return response.json();
}
```

### WebSocket
```typescript
// Пример WebSocket подключения
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  // Обработка событий от бэкенда
};
```

## 🎯 Состояния FSM

- **IDLE** - Ожидание команды
- **WAKE** - Пробуждение по wake word
- **LISTEN** - Слушает пользователя
- **THINK** - Обработка запроса
- **SPEAK** - Отвечает пользователю
- **BARGE_IN** - Прерывание ответа

## 🎨 Темы

Интерфейс поддерживает тёмную тему по умолчанию. Для добавления светлой темы:

```typescript
// В store/index.ts
updateSettings({ theme: 'light' });
```

## 📱 Адаптивность

Интерфейс полностью адаптивен:
- Desktop (1920px+)
- Laptop (1024px - 1920px)
- Tablet (768px - 1024px)
- Mobile (< 768px)

## 🔧 Разработка

### Добавление новой страницы

1. Создайте компонент в `src/pages/`
2. Добавьте маршрут в `src/App.tsx`
3. Добавьте ссылку в `src/components/layout/Sidebar.tsx`

### Добавление новой настройки

1. Добавьте поле в `Settings` тип (`src/types/index.ts`)
2. Добавьте в `defaultSettings` (`src/store/index.ts`)
3. Добавьте UI в `SettingsPage.tsx`

## 📊 Метрики

Frontend собирает следующие метрики:
- CPU usage
- RAM usage
- Количество событий
- Задержки (STT, TTS, LLM, RAG)
- Время работы (uptime)

## 🐛 Отладка

Включите debug логи:
```typescript
// В store
addLog({
  level: 'debug',
  component: 'Chat',
  message: 'Debug message',
  timestamp: new Date()
});
```

## 📝 Лицензия

MIT

---

**Создано с ❤️ для AI-ассистента Джарвис**
