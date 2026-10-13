import { phases } from '../data/roadmap';

interface Node {
  id: string;
  label: string;
  phase: number;
  priority: string;
  x: number;
  y: number;
}

interface Edge {
  from: string;
  to: string;
}

export default function DependencyView() {
  // Build nodes and edges
  const nodes: Node[] = [];
  const edges: Edge[] = [];

  const phaseY: Record<string, number> = {};
  let yCounter = 0;

  phases.forEach((phase) => {
    const baseY = yCounter;
    phaseY[phase.id] = baseY;
    phase.tasks.forEach((task, i) => {
      nodes.push({
        id: task.id,
        label: task.title.replace(/^(P\d:\s*)?/, '').substring(0, 20),
        phase: phase.number,
        priority: task.priority,
        x: i * 200 + 50,
        y: baseY * 120 + 50,
      });
    });
    yCounter += Math.ceil(phase.tasks.length / 2) + 1;
  });

  phases.forEach((phase) => {
    phase.tasks.forEach((task) => {
      task.dependencies.forEach((dep) => {
        edges.push({ from: dep, to: task.id });
      });
    });
  });

  const getNodeById = (id: string) => nodes.find(n => n.id === id);

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'P0': return '#ef4444';
      case 'P1': return '#eab308';
      case 'P2': return '#3b82f6';
      default: return '#6b7280';
    }
  };

  const getPhaseColor = (phase: number) => {
    if (phase === 0 || phase === 8) return '#22c55e';
    if (phase === 7.5) return '#eab308';
    return '#3b82f6';
  };

  // Calculate SVG dimensions
  const svgWidth = Math.max(...nodes.map(n => n.x)) + 200;
  const svgHeight = Math.max(...nodes.map(n => n.y)) + 100;

  return (
    <div className="space-y-6">
      {/* Title */}
      <div>
        <h2 className="text-2xl font-bold mb-2">🕸️ Граф зависимостей</h2>
        <p className="text-gray-400 text-sm">
          Визуализация связей между задачами. Красные — критичные (P0), жёлтые — важные (P1), синие — желательные (P2).
        </p>
      </div>

      {/* Legend */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-4">
        <div className="flex flex-wrap gap-4 items-center">
          <span className="text-xs text-gray-500">Приоритет:</span>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded-full bg-red-500"></div>
            <span className="text-xs text-gray-400">P0 (критично)</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
            <span className="text-xs text-gray-400">P1 (важно)</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-3 h-3 rounded-full bg-blue-500"></div>
            <span className="text-xs text-gray-400">P2 (желательно)</span>
          </div>
          <span className="text-xs text-gray-500 ml-4">Стрелки:</span>
          <div className="flex items-center gap-1">
            <div className="w-6 h-0.5 bg-gray-500"></div>
            <span className="text-xs text-gray-400">зависит от</span>
          </div>
        </div>
      </div>

      {/* Graph */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-4 overflow-x-auto">
        <svg width={svgWidth} height={svgHeight} className="min-w-[800px]">
          {/* Edges */}
          {edges.map((edge, i) => {
            const fromNode = getNodeById(edge.from);
            const toNode = getNodeById(edge.to);
            if (!fromNode || !toNode) return null;
            return (
              <g key={i}>
                <line
                  x1={fromNode.x + 60}
                  y1={fromNode.y + 15}
                  x2={toNode.x}
                  y2={toNode.y + 15}
                  stroke="#4b5563"
                  strokeWidth="1.5"
                  strokeDasharray="4 2"
                  markerEnd="url(#arrowhead)"
                />
              </g>
            );
          })}

          {/* Arrow marker */}
          <defs>
            <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
              <polygon points="0 0, 10 3.5, 0 7" fill="#6b7280" />
            </marker>
          </defs>

          {/* Nodes */}
          {nodes.map((node) => (
            <g key={node.id}>
              <rect
                x={node.x}
                y={node.y}
                width={120}
                height={30}
                rx={6}
                fill="#1f2937"
                stroke={getPriorityColor(node.priority)}
                strokeWidth="2"
              />
              <circle
                cx={node.x + 12}
                cy={node.y + 15}
                r={4}
                fill={getPhaseColor(node.phase)}
              />
              <text
                x={node.x + 22}
                y={node.y + 19}
                fontSize="9"
                fill="#e5e7eb"
                fontFamily="monospace"
              >
                {node.label}
              </text>
            </g>
          ))}

          {/* Phase labels */}
          {phases.map((phase) => {
            const firstTask = nodes.find(n => n.phase === phase.number);
            if (!firstTask) return null;
            return (
              <text
                key={phase.id}
                x={10}
                y={firstTask.y + 19}
                fontSize="10"
                fill={getPhaseColor(phase.number)}
                fontWeight="bold"
              >
                Ф{phase.number}
              </text>
            );
          })}
        </svg>
      </div>

      {/* Critical Path */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
        <h3 className="font-bold mb-4">🔴 Критический путь</h3>
        <p className="text-xs text-gray-500 mb-4">
          Самая длинная цепочка зависимостей — определяет минимальное время до готовности
        </p>
        <div className="flex flex-wrap items-center gap-2">
          {[
            { label: 'Tool-calling', phase: 'Ф0' },
            { label: 'llama-cpp', phase: 'Ф1' },
            { label: 'Qwen2.5-3B', phase: 'Ф1' },
            { label: 'GBNF Grammar', phase: 'Ф1' },
            { label: 'Event Bus', phase: 'Ф2' },
            { label: 'FSM', phase: 'Ф2' },
            { label: 'Capture', phase: 'Ф3' },
            { label: 'VAD', phase: 'Ф3' },
            { label: 'STT', phase: 'Ф3' },
            { label: 'TTS Waver', phase: 'Ф4' },
            { label: 'Streaming', phase: 'Ф4' },
            { label: 'Playback', phase: 'Ф4' },
            { label: 'AEC', phase: 'Ф4.5' },
            { label: 'Barge-in', phase: 'Ф4.5' },
          ].map((item, i) => (
            <div key={i} className="flex items-center gap-1">
              <div className="bg-red-900/30 border border-red-800 rounded-lg px-2 py-1 text-center">
                <div className="text-[10px] font-bold text-red-400">{item.label}</div>
                <div className="text-[8px] text-red-500/70">{item.phase}</div>
              </div>
              {i < 13 && <span className="text-red-600">→</span>}
            </div>
          ))}
        </div>
      </div>

      {/* Parallel Paths */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
        <h3 className="font-bold mb-4">🔀 Параллельные пути</h3>
        <p className="text-xs text-gray-500 mb-4">
          Задачи, которые можно делать одновременно для ускорения
        </p>
        <div className="grid md:grid-cols-3 gap-4">
          <div className="bg-blue-900/20 border border-blue-800/50 rounded-lg p-3">
            <h4 className="text-xs font-bold text-blue-400 mb-2">Путь A: Голос</h4>
            <div className="space-y-1">
              {['Capture → VAD → STT', 'TTS → Streaming → Playback', 'AEC → Barge-in'].map((s, i) => (
                <div key={i} className="text-[10px] text-gray-400 font-mono">{s}</div>
              ))}
            </div>
          </div>
          <div className="bg-purple-900/20 border border-purple-800/50 rounded-lg p-3">
            <h4 className="text-xs font-bold text-purple-400 mb-2">Путь B: Память</h4>
            <div className="space-y-1">
              {['Ingestion → Chunking', 'Embedder → RAG', 'LRU Cache'].map((s, i) => (
                <div key={i} className="text-[10px] text-gray-400 font-mono">{s}</div>
              ))}
            </div>
          </div>
          <div className="bg-green-900/20 border border-green-800/50 rounded-lg p-3">
            <h4 className="text-xs font-bold text-green-400 mb-2">Путь C: Безопасность</h4>
            <div className="space-y-1">
              {['MCP → Scopes', 'AES-GCM', 'Update/Backup'].map((s, i) => (
                <div key={i} className="text-[10px] text-gray-400 font-mono">{s}</div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
