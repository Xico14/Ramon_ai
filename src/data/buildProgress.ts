export interface BuildFile {
  path: string;
  description: string;
  phase: number;
  status: 'done' | 'in_progress' | 'planned';
  lines?: number;
}

export interface BuildPhase {
  phase: number;
  title: string;
  status: 'done' | 'in_progress' | 'planned';
  files: BuildFile[];
}

export const buildProgress: BuildPhase[] = [
  {
    phase: 0,
    title: 'Фаза 0: Proof of Concept',
    status: 'done',
    files: [
      { path: 'jarvis/requirements.txt', description: 'Зависимости проекта (обновлено)', phase: 0, status: 'done', lines: 35 },
      { path: 'jarvis/requirements-minimal.txt', description: 'Минимальные зависимости', phase: 0, status: 'done', lines: 10 },
      { path: 'jarvis/config.yaml', description: 'Конфигурация системы', phase: 0, status: 'done', lines: 85 },
      { path: 'jarvis/README.md', description: 'Документация проекта', phase: 0, status: 'done', lines: 150 },
      { path: 'jarvis/INSTALL.md', description: 'Инструкция по установке', phase: 0, status: 'done', lines: 200 },
      { path: 'jarvis/scripts/test_phase0.py', description: 'Тесты Фазы 0', phase: 0, status: 'done', lines: 180 },
      { path: 'jarvis/scripts/install.py', description: 'Скрипт установки', phase: 0, status: 'done', lines: 150 },
      { path: 'jarvis/scripts/check_project.py', description: 'Проверка структуры', phase: 0, status: 'done', lines: 150 },
      { path: 'jarvis/scripts/test_event_bus.py', description: 'Тест EventBus', phase: 0, status: 'done', lines: 100 },
    ],
  },
  {
    phase: 0,
    title: 'Фаза 0: Тесты пройдены (3/4)',
    status: 'done',
    files: [
      { path: 'jarvis/scripts/optimize_stt.py', description: 'Скрипт оптимизации STT', phase: 0, status: 'done', lines: 150 },
    ],
  },
  {
    phase: 1,
    title: 'Фаза 1: Фундамент (Мозг) — В ПРОЦЕССЕ',
    status: 'in_progress',
    files: [
      { path: 'jarvis/brain/__init__.py', description: 'Brain package', phase: 1, status: 'done', lines: 5 },
      { path: 'jarvis/brain/llm.py', description: 'LLM обёртка (llama-cpp)', phase: 1, status: 'done', lines: 175 },
      { path: 'jarvis/grammars/response.gbnf', description: 'GBNF Grammar для JSON', phase: 1, status: 'done', lines: 20 },
    ],
  },
  {
    phase: 2,
    title: 'Фаза 2: Тело и Нервы (Core)',
    status: 'done',
    files: [
      { path: 'jarvis/core/__init__.py', description: 'Core package', phase: 2, status: 'done', lines: 12 },
      { path: 'jarvis/core/config.py', description: 'Загрузка конфигурации', phase: 2, status: 'done', lines: 30 },
      { path: 'jarvis/core/event_bus.py', description: 'Event Bus + DLQ', phase: 2, status: 'done', lines: 185 },
      { path: 'jarvis/core/fsm.py', description: 'FSM (6 состояний)', phase: 2, status: 'done', lines: 165 },
      { path: 'jarvis/core/orchestrator.py', description: 'Orchestrator', phase: 2, status: 'done', lines: 170 },
      { path: 'jarvis/ui/__init__.py', description: 'UI package', phase: 2, status: 'done', lines: 2 },
      { path: 'jarvis/ui/main_window.py', description: 'PyQt6 UI', phase: 2, status: 'done', lines: 155 },
    ],
  },
  {
    phase: 3,
    title: 'Фаза 3: Слух (STT)',
    status: 'done',
    files: [
      { path: 'jarvis/audio/__init__.py', description: 'Audio package', phase: 3, status: 'done', lines: 7 },
      { path: 'jarvis/audio/capture.py', description: 'Захват звука (16 kHz)', phase: 3, status: 'done', lines: 145 },
      { path: 'jarvis/audio/vad.py', description: 'VAD (Silero v5)', phase: 3, status: 'done', lines: 175 },
      { path: 'jarvis/audio/stt.py', description: 'STT (faster-whisper)', phase: 3, status: 'done', lines: 140 },
    ],
  },
  {
    phase: 4,
    title: 'Фаза 4: Голос (TTS)',
    status: 'done',
    files: [
      { path: 'jarvis/audio/tts.py', description: 'TTS Streaming', phase: 4, status: 'done', lines: 170 },
    ],
  },
  {
    phase: 4.5,
    title: 'Фаза 4.5: Рефлексы (AEC + Barge-in) — ЗАВЕРШЕНА',
    status: 'done',
    files: [
      { path: 'jarvis/audio/aec.py', description: 'AEC (подавление эхо)', phase: 4.5, status: 'done', lines: 165 },
      { path: 'jarvis/core/orchestrator.py', description: 'Orchestrator v2 (с Barge-in)', phase: 4.5, status: 'done', lines: 260 },
      { path: 'jarvis/scripts/test_phase45.py', description: 'Тесты Фазы 4.5', phase: 4.5, status: 'done', lines: 230 },
    ],
  },
  {
    phase: 5,
    title: 'Фаза 5: Пробуждение',
    status: 'done',
    files: [
      { path: 'jarvis/audio/wake_word.py', description: 'Wake Word Detection', phase: 5, status: 'done', lines: 120 },
    ],
  },
  {
    phase: 6,
    title: 'Фаза 6: Память (RAG) — ЗАВЕРШЕНА',
    status: 'done',
    files: [
      { path: 'jarvis/rag/__init__.py', description: 'RAG package', phase: 6, status: 'done', lines: 10 },
      { path: 'jarvis/rag/ingestion.py', description: 'Загрузка документов (PDF, TXT, MD, DOCX)', phase: 6, status: 'done', lines: 180 },
      { path: 'jarvis/rag/chunker.py', description: 'Разбиение на чанки с перекрытием', phase: 6, status: 'done', lines: 140 },
      { path: 'jarvis/rag/embedder.py', description: 'Векторизация текста (sentence-transformers)', phase: 6, status: 'done', lines: 110 },
      { path: 'jarvis/rag/search.py', description: 'Гибридный поиск (BM25 + Vector + LRU Cache)', phase: 6, status: 'done', lines: 250 },
      { path: 'jarvis/scripts/test_phase6.py', description: 'Тесты Фазы 6', phase: 6, status: 'done', lines: 300 },
      { path: 'jarvis/docs/PHASE_6.md', description: 'Документация Фазы 6', phase: 6, status: 'done', lines: 200 },
    ],
  },
  {
    phase: 7,
    title: 'Фаза 7: Безопасность — ЗАВЕРШЕНА',
    status: 'done',
    files: [
      { path: 'jarvis/security/__init__.py', description: 'Security package', phase: 7, status: 'done', lines: 10 },
      { path: 'jarvis/security/mcp.py', description: 'MCP Server (8 инструментов)', phase: 7, status: 'done', lines: 280 },
      { path: 'jarvis/security/scopes.py', description: 'Scopes + Audit Log', phase: 7, status: 'done', lines: 250 },
      { path: 'jarvis/security/encryption.py', description: 'AES-GCM шифрование', phase: 7, status: 'done', lines: 200 },
      { path: 'jarvis/security/backup.py', description: 'Backup + Update Manager', phase: 7, status: 'done', lines: 250 },
      { path: 'jarvis/scripts/test_phase7.py', description: 'Тесты Фазы 7', phase: 7, status: 'done', lines: 300 },
      { path: 'jarvis/docs/PHASE_7.md', description: 'Документация Фазы 7', phase: 7, status: 'done', lines: 200 },
    ],
  },
  {
    phase: 8,
    title: 'Фаза 8: Упаковка',
    status: 'planned',
    files: [
      { path: 'jarvis/build.py', description: 'Nuitka build script', phase: 8, status: 'planned' },
      { path: 'jarvis/installer.spec', description: 'Installer config', phase: 8, status: 'planned' },
    ],
  },
  {
    phase: 0,
    title: 'Точка входа',
    status: 'done',
    files: [
      { path: 'jarvis/main.py', description: 'Главная точка входа', phase: 0, status: 'done', lines: 75 },
    ],
  },
];

export function getBuildStats() {
  const allFiles = buildProgress.flatMap(p => p.files);
  const done = allFiles.filter(f => f.status === 'done');
  const planned = allFiles.filter(f => f.status === 'planned');
  const totalLines = done.reduce((sum, f) => sum + (f.lines || 0), 0);

  return {
    totalFiles: allFiles.length,
    doneFiles: done.length,
    plannedFiles: planned.length,
    totalLines,
    percentDone: Math.round((done.length / allFiles.length) * 100),
  };
}
