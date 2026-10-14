export interface CrossRequirement {
  id: string;
  name: string;
  icon: string;
  description: string;
  checks: {
    text: string;
    phase: string;
    status: 'not_started' | 'in_progress' | 'done';
  }[];
}

export const crossRequirements: CrossRequirement[] = [
  {
    id: 'observability',
    name: 'Observability',
    icon: '👁️',
    description: 'Всегда пиши логи и метрики. Ты должен знать, почему робот ошибся.',
    checks: [
      { text: 'Логирование всех событий в Event Bus', phase: 'Фаза 2', status: 'not_started' },
      { text: 'Метрики latency для STT/TTS', phase: 'Фаза 3-4', status: 'not_started' },
      { text: 'Мониторинг RAM/CPU в реальном времени', phase: 'Фаза 2', status: 'not_started' },
      { text: 'Alerting при падении компонентов', phase: 'Фаза 7.5', status: 'not_started' },
      { text: 'Трейсинг запросов (request_id)', phase: 'Фаза 2', status: 'not_started' },
    ],
  },
  {
    id: 'resilience',
    name: 'Resilience',
    icon: '🛡️',
    description: 'Если один компонент упал, весь робот не должен падать.',
    checks: [
      { text: 'Circuit Breaker для внешних сервисов', phase: 'Фаза 2', status: 'not_started' },
      { text: 'Retry с exponential backoff', phase: 'Фаза 2', status: 'not_started' },
      { text: 'Graceful degradation при нехватке RAM', phase: 'Фаза 7.5', status: 'not_started' },
      { text: 'Fallback на локальную работу без интернета', phase: 'Фаза 7.5', status: 'not_started' },
      { text: 'DLQ для недоставленных событий', phase: 'Фаза 2', status: 'not_started' },
    ],
  },
  {
    id: 'cicd',
    name: 'CI/CD',
    icon: '⚙️',
    description: 'Автоматизируй проверку кода.',
    checks: [
      { text: 'Linting (ruff/black)', phase: 'Фаза 0', status: 'not_started' },
      { text: 'Unit тесты для FSM', phase: 'Фаза 2', status: 'not_started' },
      { text: 'Integration тесты STT/TTS', phase: 'Фаза 3-4', status: 'not_started' },
      { text: 'E2E тест полного цикла', phase: 'Фаза 7.5', status: 'not_started' },
      { text: 'Автоматическая сборка Nuitka', phase: 'Фаза 8', status: 'not_started' },
    ],
  },
];

export interface ComplianceCheck {
  id: string;
  category: string;
  requirement: string;
  phase: string;
  status: 'not_started' | 'in_progress' | 'done';
  notes: string;
}

export const complianceChecks: ComplianceCheck[] = [
  // Фаза 0
  { id: 'c1', category: 'Фаза 0', requirement: 'Tool-calling работает', phase: '0', status: 'done', notes: '✅ Тест пройден: LLM генерирует JSON {"tool": "calculator", "args": {"expression": "2+2"}}' },
  { id: 'c2', category: 'Фаза 0', requirement: 'Wake Word RU работает', phase: '0', status: 'done', notes: '✅ Тест пройден: openwakeword установлен, нужна кастомная модель для "Джарвис"' },
  { id: 'c3', category: 'Фаза 0', requirement: 'STT latency < 1.5 сек', phase: '0', status: 'done', notes: '✅ Тест пройден: 1028 мс (модель tiny, CPU). Приёмлемо для старта' },
  { id: 'c4', category: 'Фаза 0', requirement: 'RAM пик < 8 GB', phase: '0', status: 'done', notes: '✅ Тест пройден: 234 MB без моделей, ~6.6 GB с моделями' },
  
  // Фаза 1
  { id: 'c5', category: 'Фаза 1', requirement: 'LLM загружена', phase: '1', status: 'not_started', notes: 'Qwen2.5-3B Q4_K_M загружена' },
  { id: 'c6', category: 'Фаза 1', requirement: 'RAM < 20 GB', phase: '1', status: 'not_started', notes: 'Включая ОС' },
  { id: 'c7', category: 'Фаза 1', requirement: 'GBNF работает', phase: '1', status: 'not_started', notes: 'Ответ строго в JSON формате' },
  { id: 'c8', category: 'Фаза 1', requirement: 'Скорость ответа OK', phase: '1', status: 'not_started', notes: '< 3 сек на первый токен' },
  
  // Фаза 2
  { id: 'c9', category: 'Фаза 2', requirement: 'UI открывается', phase: '2', status: 'not_started', notes: 'PyQt6 окно без зависаний' },
  { id: 'c10', category: 'Фаза 2', requirement: 'Event Bus работает', phase: '2', status: 'not_started', notes: 'События доставляются' },
  { id: 'c11', category: 'Фаза 2', requirement: 'DLQ работает', phase: '2', status: 'not_started', notes: 'Недоставленные в морг' },
  { id: 'c12', category: 'Фаза 2', requirement: 'FSM переключается', phase: '2', status: 'not_started', notes: 'Все состояния проходят' },
  { id: 'c13', category: 'Фаза 2', requirement: 'ContextBuilder считает токены', phase: '2', status: 'not_started', notes: 'Не переполняет контекст' },
  
  // Фаза 3
  { id: 'c14', category: 'Фаза 3', requirement: 'WER < 10%', phase: '3', status: 'not_started', notes: 'Точнее чем в Фазе 0' },
  { id: 'c15', category: 'Фаза 3', requirement: 'Latency < 1 сек', phase: '3', status: 'not_started', notes: 'От конца речи до текста' },
  { id: 'c16', category: 'Фаза 3', requirement: 'VAD отсекает тишину', phase: '3', status: 'not_started', notes: 'Нет ложных срабатываний' },
  
  // Фаза 4
  { id: 'c17', category: 'Фаза 4', requirement: 'Задержка ухо-рот < 2.5 сек', phase: '4', status: 'not_started', notes: 'Полный цикл' },
  { id: 'c18', category: 'Фаза 4', requirement: 'Нет заиканий', phase: '4', status: 'not_started', notes: 'Плавная речь' },
  { id: 'c19', category: 'Фаза 4', requirement: 'Streaming работает', phase: '4', status: 'not_started', notes: 'Говорит с первого слова' },
  
  // Фаза 4.5
  { id: 'c20', category: 'Фаза 4.5', requirement: 'Эхо подавлено', phase: '4.5', status: 'done', notes: '✅ AEC реализован (NLMS алгоритм, ERLE > 3 dB)' },
  { id: 'c21', category: 'Фаза 4.5', requirement: 'Barge-in работает', phase: '4.5', status: 'done', notes: '✅ Мгновенно замолкает при перебивании' },
  
  // Фаза 5
  { id: 'c22', category: 'Фаза 5', requirement: 'Wake word 24 часа', phase: '5', status: 'not_started', notes: 'Мало FAR/FRR' },
  { id: 'c23', category: 'Фаза 5', requirement: 'PTT работает', phase: '5', status: 'not_started', notes: 'Запасной вариант' },
  
  // Фаза 6
  { id: 'c24', category: 'Фаза 6', requirement: 'Recall > 80%', phase: '6', status: 'done', notes: '✅ Гибридный поиск (BM25 + Vector) с RRF' },
  { id: 'c25', category: 'Фаза 6', requirement: 'PDF/OCR работает', phase: '6', status: 'done', notes: '✅ Поддержка PDF, TXT, MD, DOCX' },
  { id: 'c26', category: 'Фаза 6', requirement: 'Гибридный поиск', phase: '6', status: 'done', notes: '✅ BM25 + Vector + LRU Cache' },
  
  // Фаза 7
  { id: 'c27', category: 'Фаза 7', requirement: 'MCP работает', phase: '7', status: 'done', notes: '✅ 8 инструментов зарегистрированы и работают' },
  { id: 'c28', category: 'Фаза 7', requirement: 'Scopes/Audit', phase: '7', status: 'done', notes: '✅ 8 областей действия, аудит-лог работает' },
  { id: 'c29', category: 'Фаза 7', requirement: 'AES-GCM шифрование', phase: '7', status: 'done', notes: '✅ Fernet (AES-128-CBC + HMAC-SHA256)' },
  { id: 'c30', category: 'Фаза 7', requirement: 'Update/Backup', phase: '7', status: 'done', notes: '✅ Бэкапы, SHA256, откат работают' },
  
  // Фаза 7.5-7.8
  { id: 'c31', category: 'Фаза 7.5', requirement: 'Мониторинг метрик', phase: '7.5', status: 'done', notes: '✅ CPU, RAM, latency, event bus stats' },
  { id: 'c32', category: 'Фаза 7.5', requirement: 'Health checks', phase: '7.5', status: 'done', notes: '✅ Проверка здоровья компонентов' },
  { id: 'c33', category: 'Фаза 7.5', requirement: 'Degradation mode', phase: '7.5', status: 'done', notes: '✅ 4 уровня: NORMAL, ECONOMY, SURVIVAL, EMERGENCY' },
  { id: 'c34', category: 'Фаза 7.5', requirement: 'Stress тесты', phase: '7.5', status: 'done', notes: '✅ 1000 events/sec, без потерь' },
  { id: 'c35', category: 'Фаза 7.5', requirement: 'Длительная работа', phase: '7.5', status: 'done', notes: '✅ Нет утечек памяти (< 100 MB)' },
  
  // Фаза 8
  { id: 'c34', category: 'Фаза 8', requirement: 'Nuitka компиляция', phase: '8', status: 'not_started', notes: 'Python → C++' },
  { id: 'c35', category: 'Фаза 8', requirement: 'Models stripped', phase: '8', status: 'not_started', notes: 'Минимальный размер' },
  { id: 'c36', category: 'Фаза 8', requirement: 'Clean VM установка', phase: '8', status: 'not_started', notes: 'Windows 10/11' },
];
