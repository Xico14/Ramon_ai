import { buildProgress, getBuildStats } from '../data/buildProgress';

export default function BuildProgressView() {
  const stats = getBuildStats();

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'done': return '✅';
      case 'in_progress': return '🔄';
      case 'planned': return '⬜';
      default: return '❓';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'done': return 'bg-green-900/30 border-green-800 text-green-400';
      case 'in_progress': return 'bg-yellow-900/30 border-yellow-800 text-yellow-400';
      case 'planned': return 'bg-gray-800/30 border-gray-700 text-gray-500';
      default: return 'bg-gray-800 border-gray-700 text-gray-500';
    }
  };

  return (
    <div className="space-y-6">
      {/* Title */}
      <div>
        <h2 className="text-2xl font-bold mb-2">🏗️ Прогресс сборки проекта</h2>
        <p className="text-gray-400 text-sm">
          Реальный прогресс создания Python-проекта "Джарвис" по дорожной карте
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-4 text-center">
          <div className="text-2xl font-bold text-blue-400">{stats.totalFiles}</div>
          <div className="text-xs text-gray-500">Файлов всего</div>
        </div>
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-4 text-center">
          <div className="text-2xl font-bold text-green-400">{stats.doneFiles}</div>
          <div className="text-xs text-gray-500">Создано</div>
        </div>
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-4 text-center">
          <div className="text-2xl font-bold text-orange-400">{stats.plannedFiles}</div>
          <div className="text-xs text-gray-500">Запланировано</div>
        </div>
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-4 text-center">
          <div className="text-2xl font-bold text-purple-400">{stats.totalLines}</div>
          <div className="text-xs text-gray-500">Строк кода</div>
        </div>
      </div>

      {/* Overall Progress */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
        <div className="flex items-center justify-between mb-3">
          <div>
            <h3 className="font-bold">Общий прогресс</h3>
            <p className="text-xs text-gray-500">{stats.doneFiles} из {stats.totalFiles} файлов создано</p>
          </div>
          <div className="text-2xl font-bold text-green-400">{stats.percentDone}%</div>
        </div>
        <div className="w-full bg-gray-800 rounded-full h-3">
          <div
            className="bg-gradient-to-r from-green-500 to-blue-500 h-3 rounded-full transition-all duration-500"
            style={{ width: `${stats.percentDone}%` }}
          ></div>
        </div>
      </div>

      {/* Build Log */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
        <h3 className="font-bold mb-4">📋 Лог сборки</h3>
        <div className="bg-black/40 rounded-lg p-4 font-mono text-xs space-y-1 max-h-96 overflow-y-auto">
          <div className="text-green-400">[BUILD] Начало сборки проекта Джарвис...</div>
          <div className="text-gray-400">[INFO] Создание структуры проекта</div>
          <div className="text-green-400">[DONE] jarvis/requirements.txt (55 строк)</div>
          <div className="text-green-400">[DONE] jarvis/config.yaml (85 строк)</div>
          <div className="text-green-400">[DONE] jarvis/README.md (150 строк)</div>
          <div className="text-gray-400">[INFO] Фаза 0: Proof of Concept</div>
          <div className="text-green-400">[DONE] jarvis/scripts/test_phase0.py (180 строк)</div>
          <div className="text-gray-400">[INFO] Фаза 1: Фундамент (Мозг)</div>
          <div className="text-green-400">[DONE] jarvis/brain/__init__.py (5 строк)</div>
          <div className="text-green-400">[DONE] jarvis/brain/llm.py (175 строк)</div>
          <div className="text-green-400">[DONE] jarvis/grammars/response.gbnf (20 строк)</div>
          <div className="text-gray-400">[INFO] Фаза 2: Тело и Нервы (Core)</div>
          <div className="text-green-400">[DONE] jarvis/core/__init__.py (12 строк)</div>
          <div className="text-green-400">[DONE] jarvis/core/config.py (30 строк)</div>
          <div className="text-green-400">[DONE] jarvis/core/event_bus.py (185 строк)</div>
          <div className="text-green-400">[DONE] jarvis/core/fsm.py (165 строк)</div>
          <div className="text-green-400">[DONE] jarvis/core/orchestrator.py (170 строк)</div>
          <div className="text-green-400">[DONE] jarvis/ui/__init__.py (2 строки)</div>
          <div className="text-green-400">[DONE] jarvis/ui/main_window.py (155 строк)</div>
          <div className="text-gray-400">[INFO] Фаза 3: Слух (STT)</div>
          <div className="text-green-400">[DONE] jarvis/audio/__init__.py (7 строк)</div>
          <div className="text-green-400">[DONE] jarvis/audio/capture.py (145 строк)</div>
          <div className="text-green-400">[DONE] jarvis/audio/vad.py (175 строк)</div>
          <div className="text-green-400">[DONE] jarvis/audio/stt.py (140 строк)</div>
          <div className="text-gray-400">[INFO] Фаза 4: Голос (TTS)</div>
          <div className="text-green-400">[DONE] jarvis/audio/tts.py (170 строк)</div>
          <div className="text-gray-400">[INFO] Фаза 5: Пробуждение</div>
          <div className="text-green-400">[DONE] jarvis/audio/wake_word.py (120 строк)</div>
          <div className="text-gray-400">[INFO] Фаза 0: Точка входа</div>
          <div className="text-green-400">[DONE] jarvis/main.py (75 строк)</div>
          <div className="text-yellow-400">[NEXT] Фаза 4.5: Рефлексы (AEC + Barge-in)</div>
          <div className="text-yellow-400">[NEXT] Фаза 6: Память (RAG)</div>
          <div className="text-yellow-400">[NEXT] Фаза 7: Безопасность</div>
          <div className="text-yellow-400">[NEXT] Фаза 8: Упаковка</div>
          <div className="text-blue-400">[STATUS] Прогресс: {stats.percentDone}% ({stats.doneFiles}/{stats.totalFiles} файлов)</div>
        </div>
      </div>

      {/* Files by Phase */}
      <div className="space-y-4">
        {buildProgress.map((phase) => (
          <div key={`${phase.phase}-${phase.title}`} className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
            <div className="px-5 py-3 border-b border-gray-800 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className={getStatusColor(phase.status).split(' ')[0]}>
                  {getStatusIcon(phase.status)}
                </span>
                <h4 className="font-bold text-sm">{phase.title}</h4>
              </div>
              <span className={`text-xs px-2 py-0.5 rounded-full border ${getStatusColor(phase.status)}`}>
                {phase.files.filter(f => f.status === 'done').length}/{phase.files.length}
              </span>
            </div>
            <div className="p-4">
              <div className="space-y-2">
                {phase.files.map((file) => (
                  <div key={file.path} className="flex items-center gap-3 p-2 rounded-lg bg-gray-800/30 hover:bg-gray-800/50 transition-colors">
                    <span className="text-sm">{getStatusIcon(file.status)}</span>
                    <div className="flex-1 min-w-0">
                      <div className="text-xs font-mono text-gray-300 truncate">{file.path}</div>
                      <div className="text-[10px] text-gray-500">{file.description}</div>
                    </div>
                    {file.lines && (
                      <div className="text-[10px] text-gray-600">{file.lines} строк</div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Next Steps */}
      <div className="bg-gradient-to-br from-gray-900 to-blue-950 border border-gray-800 rounded-xl p-5">
        <h3 className="font-bold mb-4">🚀 Следующие шаги</h3>
        <div className="space-y-3">
          <div className="flex items-start gap-3">
            <span className="text-yellow-400 text-lg">1.</span>
            <div>
              <div className="text-sm font-medium">Фаза 4.5: WebRTC AEC + Barge-in</div>
              <div className="text-xs text-gray-500">Подавление эхо и мгновенная реакция на перебивание</div>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <span className="text-yellow-400 text-lg">2.</span>
            <div>
              <div className="text-sm font-medium">Фаза 6: RAG (долгая память)</div>
              <div className="text-xs text-gray-500">Поиск в документах: BM25 + векторный поиск</div>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <span className="text-yellow-400 text-lg">3.</span>
            <div>
              <div className="text-sm font-medium">Фаза 7: Безопасность и MCP</div>
              <div className="text-xs text-gray-500">Инструменты, скоупы, шифрование</div>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <span className="text-yellow-400 text-lg">4.</span>
            <div>
              <div className="text-sm font-medium">Фаза 8: Упаковка (Nuitka)</div>
              <div className="text-xs text-gray-500">Компиляция в exe, установка на Windows</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
