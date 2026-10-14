import { phases } from '../data/roadmap';
import { components } from '../data/architecture';
import { complianceChecks } from '../data/compliance';

interface Props {
  onNavigate: (tab: 'overview' | 'architecture' | 'roadmap' | 'dataflow' | 'dependencies' | 'metrics' | 'security' | 'installation' | 'build' | 'compliance') => void;
}

export default function OverviewView({ onNavigate }: Props) {
  const totalTasks = phases.reduce((sum, p) => sum + p.tasks.length, 0);
  const totalComponents = components.length;
  const totalChecks = complianceChecks.length;

  const stats = [
    { label: 'Фаз разработки', value: phases.length, icon: '📋', color: 'from-blue-500 to-blue-700' },
    { label: 'Задач всего', value: totalTasks, icon: '📝', color: 'from-purple-500 to-purple-700' },
    { label: 'Компонентов', value: totalComponents, icon: '🧩', color: 'from-green-500 to-green-700' },
    { label: 'Критериев проверки', value: totalChecks, icon: '✅', color: 'from-orange-500 to-orange-700' },
  ];

  const principles = [
    { icon: '👁️', title: 'Observability', desc: 'Логи, метрики, трейсинг — всегда знай, что происходит' },
    { icon: '🛡️', title: 'Resilience', desc: 'Один упал — остальные работают. Circuit Breaker + DLQ' },
    { icon: '⚙️', title: 'CI/CD', desc: 'Автоматические тесты, линтинг, сборка' },
    { icon: '🔒', title: 'Security', desc: 'AES-GCM, Scopes, Audit — безопасность на каждом шаге' },
  ];

  return (
    <div className="space-y-8">
      {/* Hero */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-gray-900 via-blue-950 to-purple-950 border border-gray-800 p-8">
        <div className="absolute inset-0 opacity-20">
          <div className="absolute top-10 left-10 w-32 h-32 bg-blue-500 rounded-full blur-3xl"></div>
          <div className="absolute bottom-10 right-10 w-40 h-40 bg-purple-500 rounded-full blur-3xl"></div>
        </div>
        <div className="relative z-10">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Строим <span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">Джарвиса</span> 🤖
          </h2>
          <p className="text-gray-300 text-lg max-w-2xl mb-6">
            Голосовой AI-ассистент, который живёт в компьютере. Слушает, говорит, читает книги 
            и управляет программами. Как Джарвис из Железного человека.
          </p>
          <div className="flex flex-wrap gap-3">
            <button
              onClick={() => onNavigate('architecture')}
              className="px-5 py-2.5 bg-blue-600 hover:bg-blue-500 rounded-lg font-medium transition-colors text-sm"
            >
              🧠 Архитектура
            </button>
            <button
              onClick={() => onNavigate('dataflow')}
              className="px-5 py-2.5 bg-cyan-600 hover:bg-cyan-500 rounded-lg font-medium transition-colors text-sm"
            >
              🔄 Поток данных
            </button>
            <button
              onClick={() => onNavigate('roadmap')}
              className="px-5 py-2.5 bg-purple-600 hover:bg-purple-500 rounded-lg font-medium transition-colors text-sm"
            >
              🗺️ Дорожная карта
            </button>
            <button
              onClick={() => onNavigate('dependencies')}
              className="px-5 py-2.5 bg-orange-600 hover:bg-orange-500 rounded-lg font-medium transition-colors text-sm"
            >
              🕸️ Зависимости
            </button>
            <button
              onClick={() => onNavigate('security')}
              className="px-5 py-2.5 bg-red-600 hover:bg-red-500 rounded-lg font-medium transition-colors text-sm"
            >
              🔐 Безопасность
            </button>
            <button
              onClick={() => onNavigate('build')}
              className="px-5 py-2.5 bg-teal-600 hover:bg-teal-500 rounded-lg font-medium transition-colors text-sm"
            >
              🏗️ Сборка
            </button>
            <button
              onClick={() => onNavigate('installation')}
              className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 rounded-lg font-medium transition-colors text-sm"
            >
              📦 Установка
            </button>
            <button
              onClick={() => onNavigate('metrics')}
              className="px-5 py-2.5 bg-yellow-600 hover:bg-yellow-500 rounded-lg font-medium transition-colors text-sm"
            >
              📊 Метрики
            </button>
            <button
              onClick={() => onNavigate('compliance')}
              className="px-5 py-2.5 bg-green-600 hover:bg-green-500 rounded-lg font-medium transition-colors text-sm"
            >
              ✅ Чеклист
            </button>
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {stats.map((stat) => (
          <div key={stat.label} className="bg-gray-900 border border-gray-800 rounded-xl p-4">
            <div className="text-2xl mb-2">{stat.icon}</div>
            <div className={`text-2xl font-bold bg-gradient-to-r ${stat.color} bg-clip-text text-transparent`}>
              {stat.value}
            </div>
            <div className="text-xs text-gray-500 mt-1">{stat.label}</div>
          </div>
        ))}
      </div>

      {/* Robot Anatomy */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
        <h3 className="text-lg font-bold mb-4">🤖 Анатомия робота</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Left: Senses */}
          <div className="space-y-2">
            <h4 className="text-xs font-bold text-blue-400 uppercase tracking-wider">Органы чувств</h4>
            <div className="bg-blue-900/20 border border-blue-800/50 rounded-lg p-3 space-y-2">
              <div className="flex items-center gap-2">
                <span>👂</span>
                <div>
                  <div className="text-xs font-medium">Уши (микрофон)</div>
                  <div className="text-[10px] text-gray-500">16 kHz, PyAudio</div>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <span>👁️</span>
                <div>
                  <div className="text-xs font-medium">VAD (Silero v5)</div>
                  <div className="text-[10px] text-gray-500">Детектор речи</div>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <span>👃</span>
                <div>
                  <div className="text-xs font-medium">Wake Word</div>
                  <div className="text-[10px] text-gray-500">Кодовое слово</div>
                </div>
              </div>
            </div>
          </div>

          {/* Center: Brain */}
          <div className="space-y-2">
            <h4 className="text-xs font-bold text-purple-400 uppercase tracking-wider">Мозг и Нервы</h4>
            <div className="bg-purple-900/20 border border-purple-800/50 rounded-lg p-3 space-y-2">
              <div className="flex items-center gap-2">
                <span>🧠</span>
                <div>
                  <div className="text-xs font-medium">LLM (Qwen2.5-3B)</div>
                  <div className="text-[10px] text-gray-500">Думает и отвечает</div>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <span>⚡</span>
                <div>
                  <div className="text-xs font-medium">Event Bus</div>
                  <div className="text-[10px] text-gray-500">Нервная система</div>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <span>🔄</span>
                <div>
                  <div className="text-xs font-medium">FSM</div>
                  <div className="text-[10px] text-gray-500">Сознание/состояния</div>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <span>📚</span>
                <div>
                  <div className="text-xs font-medium">RAG</div>
                  <div className="text-[10px] text-gray-500">Долгая память</div>
                </div>
              </div>
            </div>
          </div>

          {/* Right: Actuators */}
          <div className="space-y-2">
            <h4 className="text-xs font-bold text-green-400 uppercase tracking-wider">Исполнительные</h4>
            <div className="bg-green-900/20 border border-green-800/50 rounded-lg p-3 space-y-2">
              <div className="flex items-center gap-2">
                <span>🗣️</span>
                <div>
                  <div className="text-xs font-medium">Рот (TTS)</div>
                  <div className="text-[10px] text-gray-500">Streaming, 24 kHz</div>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <span>🤲</span>
                <div>
                  <div className="text-xs font-medium">Руки (MCP)</div>
                  <div className="text-[10px] text-gray-500">Инструменты</div>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <span>🛡️</span>
                <div>
                  <div className="text-xs font-medium">Иммунитет</div>
                  <div className="text-[10px] text-gray-500">Circuit Breaker</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Pipeline */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
        <h3 className="text-lg font-bold mb-4">🔄 Порядок строительства</h3>
        <div className="flex flex-wrap items-center gap-2">
          {[
            { step: '1', label: 'Мозг', sub: 'LLM', color: 'bg-purple-600' },
            { step: '2', label: 'Нервы', sub: 'Event Bus', color: 'bg-yellow-600' },
            { step: '3', label: 'Уши', sub: 'STT', color: 'bg-blue-600' },
            { step: '4', label: 'Рот', sub: 'TTS', color: 'bg-green-600' },
            { step: '5', label: 'Память', sub: 'RAG', color: 'bg-orange-600' },
            { step: '6', label: 'Руки', sub: 'MCP', color: 'bg-red-600' },
            { step: '7', label: 'Упаковка', sub: 'Nuitka', color: 'bg-gray-600' },
          ].map((item, i) => (
            <div key={item.step} className="flex items-center gap-2">
              <div className={`${item.color} rounded-lg px-3 py-2 text-center min-w-[80px]`}>
                <div className="text-xs font-bold">{item.label}</div>
                <div className="text-[10px] opacity-70">{item.sub}</div>
              </div>
              {i < 6 && <span className="text-gray-600">→</span>}
            </div>
          ))}
        </div>
      </div>

      {/* Principles */}
      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
        {principles.map((p) => (
          <div key={p.title} className="bg-gray-900 border border-gray-800 rounded-xl p-4 hover:border-gray-700 transition-colors">
            <div className="text-2xl mb-2">{p.icon}</div>
            <h4 className="font-bold text-sm mb-1">{p.title}</h4>
            <p className="text-xs text-gray-400">{p.desc}</p>
          </div>
        ))}
      </div>

      {/* Phase 0 Risks */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
        <h3 className="text-lg font-bold mb-4">⚠️ Риски Фазы 0 (Proof of Concept)</h3>
        <p className="text-xs text-gray-500 mb-4">Самые рискованные части — проверяем первыми, чтобы не строить на песке</p>
        <div className="grid md:grid-cols-2 gap-4">
          <div className="bg-red-900/20 border border-red-800/50 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-xs font-bold px-2 py-0.5 rounded bg-red-900/50 text-red-400 border border-red-800">P0</span>
              <span className="text-sm font-bold">Tool-calling</span>
            </div>
            <p className="text-xs text-gray-400">Может ли LLM корректно вызывать функции? Риск: модель не понимает JSON-формат</p>
            <div className="mt-2 text-[10px] text-red-400">Митигация: GBNF grammar + few-shot примеры</div>
          </div>
          <div className="bg-red-900/20 border border-red-800/50 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-xs font-bold px-2 py-0.5 rounded bg-red-900/50 text-red-400 border border-red-800">P0</span>
              <span className="text-sm font-bold">Wake Word RU</span>
            </div>
            <p className="text-xs text-gray-400">Есть ли библиотека для русского кодового слова? Риск: нет готового решения</p>
            <div className="mt-2 text-[10px] text-red-400">Митигация: OpenWakeWord + кастомная тренировка</div>
          </div>
          <div className="bg-yellow-900/20 border border-yellow-800/50 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-xs font-bold px-2 py-0.5 rounded bg-yellow-900/50 text-yellow-400 border border-yellow-800">P1</span>
              <span className="text-sm font-bold">TTS/STT скорость</span>
            </div>
            <p className="text-xs text-gray-400">Достаточно ли быстро для диалога? Риск: задержка &gt; 3 сек</p>
            <div className="mt-2 text-[10px] text-yellow-400">Митигация: streaming TTS + GPU ускорение</div>
          </div>
          <div className="bg-blue-900/20 border border-blue-800/50 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-xs font-bold px-2 py-0.5 rounded bg-blue-900/50 text-blue-400 border border-blue-800">P2</span>
              <span className="text-sm font-bold">RAM потребление</span>
            </div>
            <p className="text-xs text-gray-400">Влезет ли всё в 8 GB? Риск: OOM на слабых ПК</p>
            <div className="mt-2 text-[10px] text-blue-400">Митигация: квантизация Q4 + lazy loading</div>
          </div>
        </div>
      </div>

      {/* Tech Stack */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
        <h3 className="text-lg font-bold mb-4">🛠️ Технологический стек</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {[
            { name: 'Python 3.11+', cat: 'Язык' },
            { name: 'asyncio', cat: 'Асинхронность' },
            { name: 'llama-cpp-python', cat: 'LLM' },
            { name: 'Qwen2.5-3B', cat: 'Модель' },
            { name: 'faster-whisper', cat: 'STT' },
            { name: 'Silero v5', cat: 'VAD' },
            { name: 'PyQt6', cat: 'UI' },
            { name: 'SQLite', cat: 'БД' },
            { name: 'WebRTC', cat: 'AEC' },
            { name: 'FAISS', cat: 'Векторный поиск' },
            { name: 'Nuitka', cat: 'Компиляция' },
            { name: 'AES-GCM', cat: 'Шифрование' },
          ].map((tech) => (
            <div key={tech.name} className="flex items-center gap-2 bg-gray-800/50 rounded-lg px-3 py-2">
              <span className="text-xs text-gray-500">{tech.cat}</span>
              <span className="text-xs font-medium text-gray-200">{tech.name}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
