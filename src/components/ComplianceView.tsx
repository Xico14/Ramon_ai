import { useState } from 'react';
import { complianceChecks, crossRequirements } from '../data/compliance';

export default function ComplianceView() {
  const [checkStatuses, setCheckStatuses] = useState<Record<string, string>>({});
  const [activeSection, setActiveSection] = useState<'compliance' | 'cross'>('compliance');

  const toggleCheck = (id: string) => {
    const current = checkStatuses[id] || 'not_started';
    const next = current === 'not_started' ? 'done' : 'not_started';
    setCheckStatuses({ ...checkStatuses, [id]: next });
  };

  const getPhaseChecks = (phase: string) => {
    return complianceChecks.filter(c => c.phase === phase);
  };

  const getPhaseProgress = (phase: string) => {
    const checks = getPhaseChecks(phase);
    const done = checks.filter(c => (checkStatuses[c.id] || c.status) === 'done').length;
    return { done, total: checks.length, percent: checks.length > 0 ? Math.round((done / checks.length) * 100) : 0 };
  };

  const getOverallCompliance = () => {
    const total = complianceChecks.length;
    const done = complianceChecks.filter(c => (checkStatuses[c.id] || c.status) === 'done').length;
    return { done, total, percent: Math.round((done / total) * 100) };
  };

  const overall = getOverallCompliance();

  const phaseList = ['0', '1', '2', '3', '4', '4.5', '5', '6', '7', '7.5', '8'];

  const getPhaseLabel = (phase: string) => {
    const labels: Record<string, string> = {
      '0': 'Проверка на прочность',
      '1': 'Фундамент (Мозг)',
      '2': 'Тело и Нервы',
      '3': 'Слух (STT)',
      '4': 'Голос (TTS)',
      '4.5': 'Рефлексы (AEC)',
      '5': 'Пробуждение',
      '6': 'Долгая память (RAG)',
      '7': 'Безопасность',
      '7.5': 'Полировка',
      '8': 'Упаковка',
    };
    return labels[phase] || '';
  };

  const getPhaseIcon = (phase: string) => {
    if (phase === '0' || phase === '8') return '🟢';
    if (phase === '7.5') return '🟡';
    return '🔵';
  };

  return (
    <div className="space-y-6">
      {/* Title */}
      <div>
        <h2 className="text-2xl font-bold mb-2">✅ Проверка соответствия плану</h2>
        <p className="text-gray-400 text-sm">
          Убедитесь, что всё реализовано согласно плану на 100%. Отмечайте выполненные критерии.
        </p>
      </div>

      {/* Toggle */}
      <div className="flex gap-2">
        <button
          onClick={() => setActiveSection('compliance')}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
            activeSection === 'compliance' ? 'bg-blue-600 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
          }`}
        >
          📋 Чеклист по фазам
        </button>
        <button
          onClick={() => setActiveSection('cross')}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
            activeSection === 'cross' ? 'bg-blue-600 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
          }`}
        >
          🔧 Сквозные требования
        </button>
      </div>

      {activeSection === 'compliance' ? (
        <>
          {/* Overall Compliance */}
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
            <div className="flex items-center justify-between mb-3">
              <div>
                <h3 className="font-bold">Соответствие плану</h3>
                <p className="text-xs text-gray-500">{overall.done} из {overall.total} критериев выполнено</p>
              </div>
              <div className={`text-2xl font-bold ${
                overall.percent === 100 ? 'text-green-400' : overall.percent > 50 ? 'text-yellow-400' : 'text-red-400'
              }`}>
                {overall.percent}%
              </div>
            </div>
            <div className="w-full bg-gray-800 rounded-full h-3">
              <div
                className={`h-3 rounded-full transition-all duration-500 ${
                  overall.percent === 100 ? 'bg-green-500' : overall.percent > 50 ? 'bg-yellow-500' : 'bg-red-500'
                }`}
                style={{ width: `${overall.percent}%` }}
              ></div>
            </div>
          </div>

          {/* Phase Progress Bars */}
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
            <h3 className="font-bold mb-4">📊 Прогресс по фазам</h3>
            <div className="space-y-3">
              {phaseList.map((phase) => {
                const progress = getPhaseProgress(phase);
                return (
                  <div key={phase} className="flex items-center gap-3">
                    <span className="text-sm w-6">{getPhaseIcon(phase)}</span>
                    <span className="text-xs text-gray-400 w-12 font-mono">Ф{phase}</span>
                    <div className="flex-1">
                      <div className="w-full bg-gray-800 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full transition-all ${
                            progress.percent === 100 ? 'bg-green-500' : progress.percent > 0 ? 'bg-blue-500' : 'bg-gray-700'
                          }`}
                          style={{ width: `${progress.percent}%` }}
                        ></div>
                      </div>
                    </div>
                    <span className="text-xs text-gray-500 w-12 text-right">{progress.done}/{progress.total}</span>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Phase Checklists */}
          <div className="space-y-4">
            {phaseList.map((phase) => {
              const checks = getPhaseChecks(phase);
              if (checks.length === 0) return null;
              const progress = getPhaseProgress(phase);

              return (
                <div key={phase} className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
                  <div className="px-5 py-3 border-b border-gray-800 flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span>{getPhaseIcon(phase)}</span>
                      <h4 className="font-bold text-sm">Фаза {phase}: {getPhaseLabel(phase)}</h4>
                    </div>
                    <span className={`text-xs px-2 py-0.5 rounded-full ${
                      progress.percent === 100 ? 'bg-green-900/30 text-green-400' :
                      progress.percent > 0 ? 'bg-yellow-900/30 text-yellow-400' :
                      'bg-gray-800 text-gray-500'
                    }`}>
                      {progress.percent}%
                    </span>
                  </div>
                  <div className="p-4 space-y-2">
                    {checks.map((check) => {
                      const isDone = (checkStatuses[check.id] || check.status) === 'done';
                      return (
                        <div
                          key={check.id}
                          onClick={() => toggleCheck(check.id)}
                          className={`flex items-start gap-3 p-2 rounded-lg cursor-pointer transition-all hover:bg-gray-800/50 ${
                            isDone ? 'opacity-60' : ''
                          }`}
                        >
                          <div className={`w-5 h-5 rounded border-2 flex items-center justify-center flex-shrink-0 mt-0.5 transition-all ${
                            isDone ? 'bg-green-600 border-green-500' : 'border-gray-600'
                          }`}>
                            {isDone && <span className="text-white text-xs">✓</span>}
                          </div>
                          <div className="flex-1">
                            <div className={`text-sm ${isDone ? 'line-through text-gray-500' : 'text-gray-200'}`}>
                              {check.requirement}
                            </div>
                            <div className="text-xs text-gray-600 mt-0.5">{check.notes}</div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              );
            })}
          </div>
        </>
      ) : (
        /* Cross Requirements */
        <div className="space-y-4">
          {crossRequirements.map((req) => (
            <div key={req.id} className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <div className="flex items-center gap-3 mb-3">
                <span className="text-2xl">{req.icon}</span>
                <div>
                  <h3 className="font-bold">{req.name}</h3>
                  <p className="text-xs text-gray-500">{req.description}</p>
                </div>
              </div>
              <div className="space-y-2">
                {req.checks.map((check, i) => (
                  <div key={i} className="flex items-center gap-3 p-2 rounded-lg bg-gray-800/30">
                    <span className="text-gray-600">⬜</span>
                    <span className="text-sm text-gray-300 flex-1">{check.text}</span>
                    <span className="text-[10px] text-gray-600 bg-gray-800 px-2 py-0.5 rounded">{check.phase}</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Summary */}
      <div className="bg-gradient-to-br from-gray-900 to-blue-950 border border-gray-800 rounded-xl p-6">
        <h3 className="font-bold mb-3">📝 Итоговая проверка</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-black/30 rounded-lg p-3 text-center">
            <div className="text-2xl font-bold text-blue-400">{overall.percent}%</div>
            <div className="text-xs text-gray-500">Соответствие плану</div>
          </div>
          <div className="bg-black/30 rounded-lg p-3 text-center">
            <div className="text-2xl font-bold text-green-400">{overall.done}</div>
            <div className="text-xs text-gray-500">Критериев выполнено</div>
          </div>
          <div className="bg-black/30 rounded-lg p-3 text-center">
            <div className="text-2xl font-bold text-orange-400">{overall.total - overall.done}</div>
            <div className="text-xs text-gray-500">Осталось выполнить</div>
          </div>
        </div>
        {overall.percent === 100 && (
          <div className="mt-4 text-center text-green-400 font-bold">
            🎉 Поздравляем! План реализован на 100%!
          </div>
        )}
      </div>
    </div>
  );
}
