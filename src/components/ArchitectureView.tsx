import { useState } from 'react';
import { components, categoryColors, type Component } from '../data/architecture';

export default function ArchitectureView() {
  const [selectedComponent, setSelectedComponent] = useState<Component | null>(null);
  const [filter, setFilter] = useState<string>('all');

  const categories = [
    { id: 'all', label: 'Все', icon: '🔮' },
    { id: 'eventbus', label: 'Event Bus', icon: '⚡' },
    { id: 'input', label: 'Ввод/Вывод', icon: '🎤' },
    { id: 'speech', label: 'Речь', icon: '🗣️' },
    { id: 'brain', label: 'Мозг', icon: '🧠' },
    { id: 'service', label: 'Сервисы', icon: '🔧' },
  ];

  const filtered = filter === 'all' ? components : components.filter(c => c.category === filter);

  return (
    <div className="space-y-6">
      {/* Title */}
      <div>
        <h2 className="text-2xl font-bold mb-2">🧠 Архитектура системы</h2>
        <p className="text-gray-400 text-sm">
          Анатомия робота: где уши, мозг, нервы и внутренние органы. Все компоненты общаются через Event Bus.
        </p>
      </div>

      {/* FSM Diagram */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
        <h3 className="text-lg font-bold mb-4">🔄 Конечный автомат (FSM)</h3>
        <div className="flex flex-wrap items-center justify-center gap-2">
          {[
            { state: 'IDLE', label: 'Спит', color: 'bg-gray-700', emoji: '😴' },
            { state: 'WAKE', label: 'Услышал', color: 'bg-yellow-700', emoji: ' 👂' },
            { state: 'LISTEN', label: 'Слушает', color: 'bg-blue-700', emoji: '🎧' },
            { state: 'THINK', label: 'Думает', color: 'bg-purple-700', emoji: '💭' },
            { state: 'SPEAK', label: 'Говорит', color: 'bg-green-700', emoji: '🗣️' },
            { state: 'BARGE-IN', label: 'Перебит', color: 'bg-red-700', emoji: '🛑' },
          ].map((s, i) => (
            <div key={s.state} className="flex items-center gap-2">
              <div className={`${s.color} rounded-lg px-3 py-2 text-center`}>
                <div className="text-lg">{s.emoji}</div>
                <div className="text-xs font-bold">{s.state}</div>
                <div className="text-[10px] opacity-70">{s.label}</div>
              </div>
              {i < 5 && <span className="text-gray-500 text-lg">→</span>}
            </div>
          ))}
        </div>
        <div className="mt-3 text-center text-xs text-gray-500">
          BARGE-IN → LISTEN (если перебили) | SPEAK → IDLE (после ответа)
        </div>
      </div>

      {/* Event Bus Diagram */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
        <h3 className="text-lg font-bold mb-4">⚡ Event Bus (Нервная система)</h3>
        <div className="relative">
          {/* Central bus */}
          <div className="flex justify-center mb-6">
            <div className="bg-yellow-900/40 border-2 border-yellow-500 rounded-full px-8 py-3 text-center">
              <div className="text-yellow-400 font-bold text-sm">EVENT BUS</div>
              <div className="text-yellow-500/70 text-[10px]">asyncio + TypedEvents + DLQ</div>
            </div>
          </div>
          {/* Connections */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {[
              { label: 'Микрофон', event: 'audio.captured', icon: '🎤' },
              { label: 'VAD', event: 'speech.detected', icon: '📢' },
              { label: 'STT', event: 'text.transcribed', icon: '📝' },
              { label: 'LLM', event: 'response.generated', icon: '🧠' },
              { label: 'TTS', event: 'audio.speaking', icon: '🔊' },
              { label: 'RAG', event: 'context.retrieved', icon: '📚' },
              { label: 'WakeWord', event: 'wake.detected', icon: '⏰' },
              { label: 'FSM', event: 'state.changed', icon: '🔄' },
            ].map((item) => (
              <div key={item.label} className="bg-gray-800/50 border border-gray-700 rounded-lg p-3 text-center">
                <div className="text-lg mb-1">{item.icon}</div>
                <div className="text-xs font-medium">{item.label}</div>
                <div className="text-[10px] text-gray-500 mt-1 font-mono">{item.event}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Filter */}
      <div className="flex flex-wrap gap-2">
        {categories.map((cat) => (
          <button
            key={cat.id}
            onClick={() => setFilter(cat.id)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
              filter === cat.id
                ? 'bg-blue-600 text-white'
                : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
            }`}
          >
            {cat.icon} {cat.label}
          </button>
        ))}
      </div>

      {/* Components Grid */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filtered.map((comp) => {
          const colors = categoryColors[comp.category];
          return (
            <div
              key={comp.id}
              onClick={() => setSelectedComponent(comp)}
              className={`${colors.bg} border ${colors.border} rounded-xl p-4 cursor-pointer hover:scale-[1.02] transition-transform`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${colors.text} bg-black/30`}>
                  {colors.label}
                </span>
                <span className="text-[10px] text-gray-500">Фаза {comp.phase}</span>
              </div>
              <h4 className="font-bold text-sm mb-1">{comp.name}</h4>
              <p className="text-xs text-gray-400 mb-3">{comp.description}</p>
              <div className="flex flex-wrap gap-1">
                {comp.tech.map((t) => (
                  <span key={t} className="text-[10px] bg-black/30 rounded px-1.5 py-0.5 text-gray-300">
                    {t}
                  </span>
                ))}
              </div>
            </div>
          );
        })}
      </div>

      {/* Detail Modal */}
      {selectedComponent && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4" onClick={() => setSelectedComponent(null)}>
          <div className="bg-gray-900 border border-gray-700 rounded-2xl p-6 max-w-md w-full" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-4">
              <span className={`text-xs font-medium px-2 py-1 rounded-full ${categoryColors[selectedComponent.category].text} bg-black/30`}>
                {categoryColors[selectedComponent.category].label}
              </span>
              <button onClick={() => setSelectedComponent(null)} className="text-gray-500 hover:text-white">✕</button>
            </div>
            <h3 className="text-xl font-bold mb-2">{selectedComponent.name}</h3>
            <p className="text-gray-400 text-sm mb-4">{selectedComponent.description}</p>
            <div className="space-y-3">
              <div>
                <div className="text-xs text-gray-500 mb-1">Технологии</div>
                <div className="flex flex-wrap gap-2">
                  {selectedComponent.tech.map((t) => (
                    <span key={t} className="text-xs bg-gray-800 rounded-lg px-2 py-1 text-gray-300">{t}</span>
                  ))}
                </div>
              </div>
              <div>
                <div className="text-xs text-gray-500 mb-1">Фаза реализации</div>
                <div className="text-sm font-medium">Фаза {selectedComponent.phase}</div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
