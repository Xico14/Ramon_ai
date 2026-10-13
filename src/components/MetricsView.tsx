export interface Metric {
  id: string;
  name: string;
  target: string;
  current: string;
  unit: string;
  phase: string;
  status: 'good' | 'warning' | 'critical' | 'not_measured';
  description: string;
}

export const metrics: Metric[] = [
  // Фаза 0
  { id: 'm1', name: 'WER (ошибка распознавания)', target: '< 15%', current: '—', unit: '%', phase: '0', status: 'not_measured', description: 'Word Error Rate на русском языке' },
  { id: 'm2', name: 'RAM пик', target: '< 8 GB', current: '—', unit: 'GB', phase: '0', status: 'not_measured', description: 'Максимальное потребление памяти' },
  { id: 'm3', name: 'Tool-calling accuracy', target: '> 90%', current: '—', unit: '%', phase: '0', status: 'not_measured', description: 'Точность вызова функций' },
  { id: 'm4', name: 'Wake Word FAR', target: '< 1/час', current: '—', unit: '/час', phase: '0', status: 'not_measured', description: 'False Acceptance Rate' },

  // Фаза 1
  { id: 'm5', name: 'RAM с LLM', target: '< 20 GB', current: '—', unit: 'GB', phase: '1', status: 'not_measured', description: 'Включая ОС + модель' },
  { id: 'm6', name: 'TTFT (Time to First Token)', target: '< 3 сек', current: '—', unit: 'сек', phase: '1', status: 'not_measured', description: 'Время до первого токена ответа' },
  { id: 'm7', name: 'Tokens/sec', target: '> 20', current: '—', unit: 'tok/s', phase: '1', status: 'not_measured', description: 'Скорость генерации' },
  { id: 'm8', name: 'GBNF compliance', target: '100%', current: '—', unit: '%', phase: '1', status: 'not_measured', description: 'Соответствие JSON формату' },

  // Фаза 2
  { id: 'm9', name: 'Event delivery rate', target: '100%', current: '—', unit: '%', phase: '2', status: 'not_measured', description: 'Доставляемость событий (без DLQ)' },
  { id: 'm10', name: 'FSM transitions/sec', target: '> 100', current: '—', unit: '/сек', phase: '2', status: 'not_measured', description: 'Скорость переключения состояний' },
  { id: 'm11', name: 'UI FPS', target: '> 30', current: '—', unit: 'FPS', phase: '2', status: 'not_measured', description: 'Плавность интерфейса' },

  // Фаза 3
  { id: 'm12', name: 'WER (production)', target: '< 10%', current: '—', unit: '%', phase: '3', status: 'not_measured', description: 'Точнее чем в Фазе 0' },
  { id: 'm13', name: 'STT latency', target: '< 1 сек', current: '—', unit: 'мс', phase: '3', status: 'not_measured', description: 'От конца речи до текста' },
  { id: 'm14', name: 'VAD false positive', target: '< 2%', current: '—', unit: '%', phase: '3', status: 'not_measured', description: 'Ложные срабатывания детектора' },

  // Фаза 4
  { id: 'm15', name: 'Ear-to-mouth latency', target: '< 2.5 сек', current: '—', unit: 'мс', phase: '4', status: 'not_measured', description: 'Полный цикл ухо→рот' },
  { id: 'm16', name: 'TTS glitches', target: '0', current: '—', unit: '/мин', phase: '4', status: 'not_measured', description: 'Заикания и артефакты' },
  { id: 'm17', name: 'Audio quality MOS', target: '> 3.5', current: '—', unit: 'MOS', phase: '4', status: 'not_measured', description: 'Mean Opinion Score качества звука' },

  // Фаза 4.5
  { id: 'm18', name: 'Echo return loss (ERLE)', target: '> 30 dB', current: '—', unit: 'dB', phase: '4.5', status: 'not_measured', description: 'Подавление эхо' },
  { id: 'm19', name: 'Barge-in reaction', target: '< 200 мс', current: '—', unit: 'мс', phase: '4.5', status: 'not_measured', description: 'Время реакции на перебивание' },

  // Фаза 5
  { id: 'm20', name: 'Wake Word FAR (24h)', target: '< 0.5/час', current: '—', unit: '/час', phase: '5', status: 'not_measured', description: 'Ложные срабатывания за 24 часа' },
  { id: 'm21', name: 'Wake Word FRR', target: '< 5%', current: '—', unit: '%', phase: '5', status: 'not_measured', description: 'False Rejection Rate' },

  // Фаза 6
  { id: 'm22', name: 'RAG Recall@5', target: '> 80%', current: '—', unit: '%', phase: '6', status: 'not_measured', description: 'Точность поиска в топ-5' },
  { id: 'm23', name: 'RAG latency', target: '< 200 мс', current: '—', unit: 'мс', phase: '6', status: 'not_measured', description: 'Время поиска в документах' },
  { id: 'm24', name: 'Cache hit rate', target: '> 30%', current: '—', unit: '%', phase: '6', status: 'not_measured', description: 'Попадания в LRU кэш' },

  // Фаза 7
  { id: 'm25', name: 'Tool success rate', target: '> 95%', current: '—', unit: '%', phase: '7', status: 'not_measured', description: 'Успешность вызова инструментов' },
  { id: 'm26', name: 'Encryption overhead', target: '< 5%', current: '—', unit: '%', phase: '7', status: 'not_measured', description: 'Накладные расходы AES-GCM' },

  // Фаза 7.5
  { id: 'm27', name: 'Stability (8h)', target: '0 crashes', current: '—', unit: '', phase: '7.5', status: 'not_measured', description: 'Стабильность за 8 часов' },
  { id: 'm28', name: 'Memory leak', target: '< 50 MB/час', current: '—', unit: 'MB/ч', phase: '7.5', status: 'not_measured', description: 'Утечка памяти' },
  { id: 'm29', name: 'CPU idle', target: '< 5%', current: '—', unit: '%', phase: '7.5', status: 'not_measured', description: 'CPU в режиме ожидания' },

  // Фаза 8
  { id: 'm30', name: 'Install size', target: '< 4 GB', current: '—', unit: 'GB', phase: '8', status: 'not_measured', description: 'Размер дистрибутива' },
  { id: 'm31', name: 'Cold start', target: '< 30 сек', current: '—', unit: 'сек', phase: '8', status: 'not_measured', description: 'Время запуска с нуля' },
  { id: 'm32', name: 'Clean install success', target: '100%', current: '—', unit: '%', phase: '8', status: 'not_measured', description: 'Установка на чистой Windows' },
];

export default function MetricsView() {
  const phaseGroups = [...new Set(metrics.map(m => m.phase))];

  const getPhaseLabel = (phase: string) => {
    const labels: Record<string, string> = {
      '0': 'Фаза 0: Проверка на прочность',
      '1': 'Фаза 1: Мозг (LLM)',
      '2': 'Фаза 2: Тело и Нервы',
      '3': 'Фаза 3: Слух (STT)',
      '4': 'Фаза 4: Голос (TTS)',
      '4.5': 'Фаза 4.5: Рефлексы',
      '5': 'Фаза 5: Пробуждение',
      '6': 'Фаза 6: Память (RAG)',
      '7': 'Фаза 7: Безопасность',
      '7.5': 'Фаза 7.5: Полировка',
      '8': 'Фаза 8: Упаковка',
    };
    return labels[phase] || `Фаза ${phase}`;
  };

  const getPhaseIcon = (phase: string) => {
    if (phase === '0' || phase === '8') return '🟢';
    if (phase === '7.5') return '🟡';
    return '🔵';
  };

  const totalMetrics = metrics.length;
  const measured = metrics.filter(m => m.status !== 'not_measured').length;

  return (
    <div className="space-y-6">
      {/* Title */}
      <div>
        <h2 className="text-2xl font-bold mb-2">📊 Метрики и KPI</h2>
        <p className="text-gray-400 text-sm">
          Конкретные измеримые цели для каждой вехи. Без метрик нет управления.
        </p>
      </div>

      {/* Summary */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-4 text-center">
          <div className="text-2xl font-bold text-blue-400">{totalMetrics}</div>
          <div className="text-xs text-gray-500">Всего метрик</div>
        </div>
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-4 text-center">
          <div className="text-2xl font-bold text-green-400">{measured}</div>
          <div className="text-xs text-gray-500">Измерено</div>
        </div>
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-4 text-center">
          <div className="text-2xl font-bold text-orange-400">{totalMetrics - measured}</div>
          <div className="text-xs text-gray-500">Ожидает измерения</div>
        </div>
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-4 text-center">
          <div className="text-2xl font-bold text-purple-400">{phaseGroups.length}</div>
          <div className="text-xs text-gray-500">Фаз с метриками</div>
        </div>
      </div>

      {/* Key Metrics Highlight */}
      <div className="bg-gradient-to-br from-gray-900 to-blue-950 border border-gray-800 rounded-xl p-6">
        <h3 className="font-bold mb-4">🎯 Ключевые метрики системы</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-black/30 rounded-lg p-4 border border-gray-700">
            <div className="text-xs text-gray-500 mb-1">Полная задержка</div>
            <div className="text-xl font-bold text-green-400">&lt; 2.5 сек</div>
            <div className="text-xs text-gray-500 mt-1">Ухо → Рот (end-to-end)</div>
          </div>
          <div className="bg-black/30 rounded-lg p-4 border border-gray-700">
            <div className="text-xs text-gray-500 mb-1">Точность речи</div>
            <div className="text-xl font-bold text-blue-400">WER &lt; 10%</div>
            <div className="text-xs text-gray-500 mt-1">Распознавание русского</div>
          </div>
          <div className="bg-black/30 rounded-lg p-4 border border-gray-700">
            <div className="text-xs text-gray-500 mb-1">Поиск в памяти</div>
            <div className="text-xl font-bold text-purple-400">Recall &gt; 80%</div>
            <div className="text-xs text-gray-500 mt-1">RAG точность</div>
          </div>
        </div>
      </div>

      {/* Metrics by Phase */}
      <div className="space-y-4">
        {phaseGroups.map((phase) => {
          const phaseMetrics = metrics.filter(m => m.phase === phase);
          return (
            <div key={phase} className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
              <div className="px-5 py-3 border-b border-gray-800 flex items-center gap-2">
                <span>{getPhaseIcon(phase)}</span>
                <h4 className="font-bold text-sm">{getPhaseLabel(phase)}</h4>
                <span className="text-xs text-gray-500 ml-auto">{phaseMetrics.length} метрик</span>
              </div>
              <div className="p-4">
                <div className="grid gap-2">
                  {phaseMetrics.map((metric) => (
                    <div key={metric.id} className="flex items-center gap-3 p-2 rounded-lg bg-gray-800/30 hover:bg-gray-800/50 transition-colors">
                      <div className="w-2 h-2 rounded-full bg-gray-600 flex-shrink-0"></div>
                      <div className="flex-1 min-w-0">
                        <div className="text-sm font-medium text-gray-200">{metric.name}</div>
                        <div className="text-xs text-gray-500 truncate">{metric.description}</div>
                      </div>
                      <div className="text-right flex-shrink-0">
                        <div className="text-xs font-bold text-green-400">{metric.target}</div>
                        <div className="text-[10px] text-gray-600">
                          {metric.status === 'not_measured' ? 'ожидает' : metric.current}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Resource Budget */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
        <h3 className="font-bold mb-4">💾 Бюджет ресурсов</h3>
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h4 className="text-sm font-medium text-gray-400 mb-3">RAM (оперативная память)</h4>
            <div className="space-y-2">
              {[
                { label: 'ОС + фон', size: 2, color: 'bg-gray-600' },
                { label: 'LLM (Qwen2.5-3B Q4)', size: 3.5, color: 'bg-purple-600' },
                { label: 'STT (faster-whisper)', size: 2, color: 'bg-blue-600' },
                { label: 'TTS модель', size: 1.5, color: 'bg-green-600' },
                { label: 'Embeddings + RAG', size: 1, color: 'bg-orange-600' },
                { label: 'UI + буферы', size: 1, color: 'bg-pink-600' },
              ].map((item) => (
                <div key={item.label} className="flex items-center gap-2">
                  <div className={`w-3 h-3 rounded ${item.color}`}></div>
                  <span className="text-xs text-gray-400 flex-1">{item.label}</span>
                  <span className="text-xs font-mono text-gray-300">{item.size} GB</span>
                </div>
              ))}
              <div className="border-t border-gray-700 pt-2 mt-2 flex items-center gap-2">
                <span className="text-xs font-bold text-gray-300 flex-1">ИТОГО</span>
                <span className="text-sm font-bold text-yellow-400">~11 GB</span>
              </div>
            </div>
          </div>
          <div>
            <h4 className="text-sm font-medium text-gray-400 mb-3">Диск (постоянная память)</h4>
            <div className="space-y-2">
              {[
                { label: 'LLM модель (Q4_K_M)', size: 2.0, color: 'bg-purple-600' },
                { label: 'Whisper large-v3', size: 3.0, color: 'bg-blue-600' },
                { label: 'TTS модель', size: 1.0, color: 'bg-green-600' },
                { label: 'Embeddings модель', size: 0.5, color: 'bg-orange-600' },
                { label: 'VAD (Silero)', size: 0.05, color: 'bg-cyan-600' },
                { label: 'Python + зависимости', size: 1.0, color: 'bg-gray-600' },
                { label: 'Nuitka binary', size: 0.5, color: 'bg-red-600' },
              ].map((item) => (
                <div key={item.label} className="flex items-center gap-2">
                  <div className={`w-3 h-3 rounded ${item.color}`}></div>
                  <span className="text-xs text-gray-400 flex-1">{item.label}</span>
                  <span className="text-xs font-mono text-gray-300">{item.size} GB</span>
                </div>
              ))}
              <div className="border-t border-gray-700 pt-2 mt-2 flex items-center gap-2">
                <span className="text-xs font-bold text-gray-300 flex-1">ИТОГО</span>
                <span className="text-sm font-bold text-yellow-400">~8 GB</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
