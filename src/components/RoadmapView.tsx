import { useState } from 'react';
import { phases, type Phase } from '../data/roadmap';

export default function RoadmapView() {
  const [expandedPhase, setExpandedPhase] = useState<string | null>('phase0');
  const [taskStatuses, setTaskStatuses] = useState<Record<string, string>>({});

  const togglePhase = (id: string) => {
    setExpandedPhase(expandedPhase === id ? null : id);
  };

  const toggleTask = (taskId: string) => {
    const current = taskStatuses[taskId] || 'not_started';
    const next = current === 'not_started' ? 'in_progress' : current === 'in_progress' ? 'done' : 'not_started';
    setTaskStatuses({ ...taskStatuses, [taskId]: next });
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'done': return '✅';
      case 'in_progress': return '🔄';
      default: return '⬜';
    }
  };

  const getPhaseProgress = (phase: Phase) => {
    const total = phase.tasks.length;
    const done = phase.tasks.filter(t => (taskStatuses[t.id] || t.status) === 'done').length;
    return { done, total, percent: Math.round((done / total) * 100) };
  };

  const getOverallProgress = () => {
    const total = phases.reduce((sum, p) => sum + p.tasks.length, 0);
    const done = phases.reduce((sum, p) => sum + p.tasks.filter(t => (taskStatuses[t.id] || t.status) === 'done').length, 0);
    return { done, total, percent: Math.round((done / total) * 100) };
  };

  const overall = getOverallProgress();

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'P0': return 'text-red-400 bg-red-900/30 border-red-800';
      case 'P1': return 'text-yellow-400 bg-yellow-900/30 border-yellow-800';
      case 'P2': return 'text-blue-400 bg-blue-900/30 border-blue-800';
      default: return 'text-gray-400 bg-gray-900/30 border-gray-800';
    }
  };

  return (
    <div className="space-y-6">
      {/* Title */}
      <div>
        <h2 className="text-2xl font-bold mb-2">🗺️ Дорожная карта</h2>
        <p className="text-gray-400 text-sm">
          План строительства от простого к сложному. Нажимайте на задачи для изменения статуса.
        </p>
      </div>

      {/* Overall Progress */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
        <div className="flex items-center justify-between mb-3">
          <div>
            <h3 className="font-bold">Общий прогресс</h3>
            <p className="text-xs text-gray-500">{overall.done} из {overall.total} задач выполнено</p>
          </div>
          <div className="text-2xl font-bold text-blue-400">{overall.percent}%</div>
        </div>
        <div className="w-full bg-gray-800 rounded-full h-3">
          <div
            className="bg-gradient-to-r from-blue-500 to-purple-500 h-3 rounded-full transition-all duration-500"
            style={{ width: `${overall.percent}%` }}
          ></div>
        </div>
      </div>

      {/* Phases Timeline */}
      <div className="space-y-3">
        {phases.map((phase) => {
          const progress = getPhaseProgress(phase);
          const isExpanded = expandedPhase === phase.id;

          return (
            <div key={phase.id} className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
              {/* Phase Header */}
              <button
                onClick={() => togglePhase(phase.id)}
                className="w-full px-5 py-4 flex items-center gap-4 hover:bg-gray-800/50 transition-colors text-left"
              >
                <span className="text-2xl">{phase.icon}</span>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs text-gray-500 font-mono">ФАЗА {phase.number}</span>
                    <span className={`text-xs px-2 py-0.5 rounded-full border ${
                      progress.percent === 100 ? 'bg-green-900/30 text-green-400 border-green-800' :
                      progress.percent > 0 ? 'bg-yellow-900/30 text-yellow-400 border-yellow-800' :
                      'bg-gray-800 text-gray-500 border-gray-700'
                    }`}>
                      {progress.done}/{progress.total}
                    </span>
                  </div>
                  <h3 className="font-bold text-sm truncate">{phase.title}</h3>
                  <p className="text-xs text-gray-500 truncate">{phase.goal}</p>
                </div>
                <div className="hidden sm:block w-24">
                  <div className="w-full bg-gray-800 rounded-full h-2">
                    <div
                      className="bg-blue-500 h-2 rounded-full transition-all"
                      style={{ width: `${progress.percent}%` }}
                    ></div>
                  </div>
                </div>
                <span className={`text-gray-500 transition-transform ${isExpanded ? 'rotate-180' : ''}`}>
                  ▼
                </span>
              </button>

              {/* Phase Content */}
              {isExpanded && (
                <div className="px-5 pb-4 border-t border-gray-800">
                  {/* Milestone */}
                  <div className="mt-3 mb-4 bg-blue-900/20 border border-blue-800/50 rounded-lg px-3 py-2">
                    <span className="text-xs text-blue-400">🎯 ВЕХА: </span>
                    <span className="text-xs text-blue-300">{phase.milestone}</span>
                  </div>

                  {/* Tasks */}
                  <div className="space-y-2">
                    {phase.tasks.map((task) => {
                      const status = taskStatuses[task.id] || task.status;
                      return (
                        <div
                          key={task.id}
                          onClick={() => toggleTask(task.id)}
                          className={`flex items-start gap-3 p-3 rounded-lg cursor-pointer transition-all hover:bg-gray-800/50 ${
                            status === 'done' ? 'opacity-60' : ''
                          }`}
                        >
                          <span className="text-lg mt-0.5">{getStatusIcon(status)}</span>
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-2 mb-0.5">
                              <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded border ${getPriorityColor(task.priority)}`}>
                                {task.priority}
                              </span>
                              <span className={`text-sm font-medium ${status === 'done' ? 'line-through text-gray-500' : ''}`}>
                                {task.title}
                              </span>
                            </div>
                            <p className="text-xs text-gray-500">{task.description}</p>
                            {task.dependencies.length > 0 && (
                              <div className="flex items-center gap-1 mt-1">
                                <span className="text-[10px] text-gray-600">Зависит от:</span>
                                {task.dependencies.map((dep) => (
                                  <span key={dep} className="text-[10px] bg-gray-800 rounded px-1.5 py-0.5 text-gray-500">
                                    {dep}
                                  </span>
                                ))}
                              </div>
                            )}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Legend */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-4">
        <h4 className="text-sm font-bold mb-3">📊 Легенда приоритетов</h4>
        <div className="flex flex-wrap gap-4">
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold px-2 py-0.5 rounded border text-red-400 bg-red-900/30 border-red-800">P0</span>
            <span className="text-xs text-gray-400">Критично — без этого не работает</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold px-2 py-0.5 rounded border text-yellow-400 bg-yellow-900/30 border-yellow-800">P1</span>
            <span className="text-xs text-gray-400">Важно — значительно улучшает</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold px-2 py-0.5 rounded border text-blue-400 bg-blue-900/30 border-blue-800">P2</span>
            <span className="text-xs text-gray-400">Желательно — можно отложить</span>
          </div>
        </div>
      </div>
    </div>
  );
}
