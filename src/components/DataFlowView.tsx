import { useState, useEffect } from 'react';

interface FlowStep {
  id: string;
  label: string;
  sublabel: string;
  icon: string;
  color: string;
  latency: string;
  tech: string;
  details: string[];
}

const flowSteps: FlowStep[] = [
  {
    id: 'mic',
    label: 'Микрофон',
    sublabel: 'Захват звука',
    icon: '🎤',
    color: 'from-blue-500 to-blue-700',
    latency: '—',
    tech: 'PyAudio, 16 kHz, Ring Buffer',
    details: ['Непрерывный захват 16 kHz', 'Кольцевой буфер 2 сек', 'Формат: PCM 16-bit mono'],
  },
  {
    id: 'aec',
    label: 'AEC',
    sublabel: 'Подавление эхо',
    icon: '🔇',
    color: 'from-red-500 to-red-700',
    latency: '~5 ms',
    tech: 'WebRTC AEC',
    details: ['Убирает свой голос из микрофона', 'Критично для barge-in', 'Работает в реальном времени'],
  },
  {
    id: 'vad',
    label: 'VAD',
    sublabel: 'Детектор речи',
    icon: '📢',
    color: 'from-green-500 to-green-700',
    latency: '~30 ms',
    tech: 'Silero v5',
    details: ['Определяет начало/конец речи', 'Отсекает тишину', 'Порог настраивается'],
  },
  {
    id: 'stt',
    label: 'STT',
    sublabel: 'Речь → Текст',
    icon: '📝',
    color: 'from-cyan-500 to-cyan-700',
    latency: '< 1 сек',
    tech: 'faster-whisper large-v3',
    details: ['GPU: ~300 ms', 'CPU: ~800 ms', 'WER < 10% на русском'],
  },
  {
    id: 'rag',
    label: 'RAG',
    sublabel: 'Поиск контекста',
    icon: '📚',
    color: 'from-orange-500 to-orange-700',
    latency: '< 200 ms',
    tech: 'BM25 + FAISS + LRU Cache',
    details: ['Гибридный поиск', 'Топ-5 чанков', 'Кэш частых запросов'],
  },
  {
    id: 'llm',
    label: 'LLM',
    sublabel: 'Генерация ответа',
    icon: '🧠',
    color: 'from-purple-500 to-purple-700',
    latency: '< 3 сек (1-й токен)',
    tech: 'Qwen2.5-3B Q4_K_M + GBNF',
    details: ['Стриминг токенов', 'JSON формат (GBNF)', 'Tool-calling'],
  },
  {
    id: 'tts',
    label: 'TTS',
    sublabel: 'Текст → Речь',
    icon: '🔊',
    color: 'from-pink-500 to-pink-700',
    latency: 'Streaming!',
    tech: 'Streaming TTS, 24 kHz',
    details: ['Начинает с 1-го слова', 'Не ждёт весь ответ', '24 kHz вывод'],
  },
  {
    id: 'speaker',
    label: 'Динамик',
    sublabel: 'Воспроизведение',
    icon: '🔈',
    color: 'from-indigo-500 to-indigo-700',
    latency: '—',
    tech: 'Playback 24 kHz',
    details: ['Непрерывное воспроизведение', 'Буферизация', 'Поддержка barge-in'],
  },
];

export default function DataFlowView() {
  const [activeStep, setActiveStep] = useState<number>(0);
  const [isAnimating, setIsAnimating] = useState(true);

  useEffect(() => {
    if (!isAnimating) return;
    const interval = setInterval(() => {
      setActiveStep((prev) => (prev + 1) % flowSteps.length);
    }, 2000);
    return () => clearInterval(interval);
  }, [isAnimating]);

  const totalLatency = '< 2.5 сек';

  return (
    <div className="space-y-6">
      {/* Title */}
      <div>
        <h2 className="text-2xl font-bold mb-2">🔄 Поток данных</h2>
        <p className="text-gray-400 text-sm">
          Как звук превращается в ответ: от микрофона до динамика. Цепочка обработки в реальном времени.
        </p>
      </div>

      {/* Animation Control */}
      <div className="flex items-center gap-3">
        <button
          onClick={() => setIsAnimating(!isAnimating)}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
            isAnimating ? 'bg-red-600 hover:bg-red-500' : 'bg-green-600 hover:bg-green-500'
          } text-white`}
        >
          {isAnimating ? '⏸ Пауза' : '▶ Запустить'}
        </button>
        <div className="text-sm text-gray-400">
          Целевая задержка <span className="font-bold text-green-400">ухо→рот</span>: {totalLatency}
        </div>
      </div>

      {/* Flow Pipeline */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 overflow-x-auto">
        <div className="flex items-center gap-1 min-w-[900px]">
          {flowSteps.map((step, i) => (
            <div key={step.id} className="flex items-center">
              <button
                onClick={() => { setActiveStep(i); setIsAnimating(false); }}
                className={`relative flex flex-col items-center p-3 rounded-xl transition-all duration-300 min-w-[100px] ${
                  i === activeStep
                    ? `bg-gradient-to-b ${step.color} scale-110 shadow-lg shadow-blue-500/20`
                    : i < activeStep
                    ? 'bg-gray-800/50 opacity-60'
                    : 'bg-gray-800/30 opacity-40'
                }`}
              >
                {/* Pulse animation for active */}
                {i === activeStep && (
                  <div className="absolute inset-0 rounded-xl animate-ping opacity-20 bg-white"></div>
                )}
                <span className="text-2xl mb-1 relative z-10">{step.icon}</span>
                <span className="text-xs font-bold relative z-10">{step.label}</span>
                <span className="text-[10px] text-gray-300 relative z-10">{step.sublabel}</span>
                {step.latency !== '—' && (
                  <span className="text-[9px] mt-1 bg-black/40 rounded px-1.5 py-0.5 relative z-10">
                    ⏱ {step.latency}
                  </span>
                )}
              </button>
              {i < flowSteps.length - 1 && (
                <div className={`mx-1 transition-all duration-300 ${i < activeStep ? 'text-green-400' : 'text-gray-700'}`}>
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M5 12h14M12 5l7 7-7 7" />
                  </svg>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Active Step Details */}
      <div className="grid md:grid-cols-2 gap-4">
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
          <div className="flex items-center gap-3 mb-4">
            <span className="text-3xl">{flowSteps[activeStep].icon}</span>
            <div>
              <h3 className="font-bold text-lg">{flowSteps[activeStep].label}</h3>
              <p className="text-sm text-gray-400">{flowSteps[activeStep].sublabel}</p>
            </div>
          </div>
          <div className="space-y-2">
            {flowSteps[activeStep].details.map((d, i) => (
              <div key={i} className="flex items-center gap-2 text-sm text-gray-300">
                <span className="text-green-400">•</span>
                {d}
              </div>
            ))}
          </div>
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
          <h4 className="font-bold text-sm mb-3 text-gray-400">🛠 Технологии</h4>
          <div className="bg-black/30 rounded-lg p-3 mb-4">
            <code className="text-sm text-blue-300">{flowSteps[activeStep].tech}</code>
          </div>
          <h4 className="font-bold text-sm mb-3 text-gray-400">⏱ Задержка</h4>
          <div className="text-2xl font-bold text-green-400">
            {flowSteps[activeStep].latency}
          </div>
          <div className="mt-4">
            <h4 className="font-bold text-sm mb-2 text-gray-400">📡 Событие Event Bus</h4>
            <code className="text-xs bg-black/30 rounded px-2 py-1 text-yellow-300">
              {flowSteps[activeStep].id}.processed → emit('{flowSteps[activeStep].id}.done')
            </code>
          </div>
        </div>
      </div>

      {/* Latency Budget */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
        <h3 className="font-bold mb-4">⏱ Бюджет задержки (Latency Budget)</h3>
        <p className="text-xs text-gray-500 mb-4">Цель: полный цикл ухо→рот &lt; 2.5 сек</p>
        <div className="space-y-2">
          {[
            { label: 'VAD detection', ms: 30, max: 50 },
            { label: 'STT (faster-whisper)', ms: 800, max: 1000 },
            { label: 'RAG retrieval', ms: 150, max: 200 },
            { label: 'LLM first token', ms: 800, max: 1500 },
            { label: 'TTS first chunk', ms: 200, max: 400 },
            { label: 'Network/buffer overhead', ms: 100, max: 200 },
          ].map((item) => (
            <div key={item.label} className="flex items-center gap-3">
              <span className="text-xs text-gray-400 w-44">{item.label}</span>
              <div className="flex-1 bg-gray-800 rounded-full h-3 relative">
                <div
                  className={`h-3 rounded-full transition-all ${
                    (item.ms / item.max) > 0.8 ? 'bg-red-500' : (item.ms / item.max) > 0.5 ? 'bg-yellow-500' : 'bg-green-500'
                  }`}
                  style={{ width: `${(item.ms / item.max) * 100}%` }}
                ></div>
                <div
                  className="absolute top-0 h-3 border-r-2 border-white/30"
                  style={{ left: '100%' }}
                ></div>
              </div>
              <span className="text-xs text-gray-500 w-20 text-right">{item.ms} ms</span>
            </div>
          ))}
          <div className="flex items-center gap-3 pt-2 border-t border-gray-800 mt-2">
            <span className="text-xs font-bold text-gray-300 w-44">ИТОГО (пайплайн)</span>
            <div className="flex-1"></div>
            <span className="text-sm font-bold text-green-400 w-20 text-right">~2080 ms</span>
          </div>
        </div>
      </div>

      {/* Barge-in Flow */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
        <h3 className="font-bold mb-4">🛑 Barge-in (перебивание)</h3>
        <div className="flex flex-wrap items-center gap-3">
          {[
            { label: 'Робот говорит', icon: '🗣️', color: 'bg-green-800' },
            { label: '→', icon: '', color: '' },
            { label: 'Пользователь начинает', icon: '👤', color: 'bg-blue-800' },
            { label: '→', icon: '', color: '' },
            { label: 'VAD обнаруживает', icon: '📢', color: 'bg-yellow-800' },
            { label: '→', icon: '', color: '' },
            { label: 'AEC подавляет эхо', icon: '🔇', color: 'bg-red-800' },
            { label: '→', icon: '', color: '' },
            { label: 'Робот замолкает', icon: '🤫', color: 'bg-purple-800' },
            { label: '→', icon: '', color: '' },
            { label: 'FSM: BARGE-IN', icon: '🔄', color: 'bg-orange-800' },
          ].map((step, i) => (
            step.icon ? (
              <div key={i} className={`${step.color} rounded-lg px-3 py-2 text-center`}>
                <div className="text-lg">{step.icon}</div>
                <div className="text-[10px]">{step.label}</div>
              </div>
            ) : (
              <span key={i} className="text-gray-600 text-lg">{step.label}</span>
            )
          ))}
        </div>
        <p className="text-xs text-gray-500 mt-3">
          ⏱ Время реакции barge-in: &lt; 200 ms от начала речи пользователя до остановки TTS
        </p>
      </div>
    </div>
  );
}
