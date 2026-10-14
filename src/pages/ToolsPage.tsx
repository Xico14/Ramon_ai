import { motion } from 'framer-motion';
import { Wrench, Shield, AlertTriangle } from 'lucide-react';
import { useAppStore } from '../store';
import { cn } from '../lib/utils';

export function ToolsPage() {
  const { tools, updateTool } = useAppStore();

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'low': return 'bg-green-500/20 text-green-500 border-green-500/50';
      case 'medium': return 'bg-yellow-500/20 text-yellow-500 border-yellow-500/50';
      case 'high': return 'bg-red-500/20 text-red-500 border-red-500/50';
      default: return 'bg-gray-500/20 text-gray-500 border-gray-500/50';
    }
  };

  const getRiskLabel = (risk: string) => {
    switch (risk) {
      case 'low': return 'Низкий';
      case 'medium': return 'Средний';
      case 'high': return 'Высокий';
      default: return 'Неизвестно';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-3xl font-bold text-white mb-2">Инструменты</h1>
        <p className="text-gray-400">Управление инструментами MCP</p>
      </motion.div>

      {/* Tools Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {tools.map((tool, index) => (
          <motion.div
            key={tool.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.05 }}
            className="bg-gray-900 border border-gray-800 rounded-xl p-6 hover:border-gray-700 transition-all"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center">
                  <Wrench className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h3 className="font-semibold text-white">{tool.name}</h3>
                  <p className="text-xs text-gray-400">{tool.scope}</p>
                </div>
              </div>
              <button
                onClick={() => updateTool(tool.id, { enabled: !tool.enabled })}
                className={cn(
                  'px-3 py-1 rounded-lg text-xs font-medium transition-colors',
                  tool.enabled
                    ? 'bg-green-500/20 text-green-500 hover:bg-green-500/30'
                    : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                )}
              >
                {tool.enabled ? 'Включен' : 'Выключен'}
              </button>
            </div>

            <p className="text-sm text-gray-400 mb-4">{tool.description}</p>

            <div className="flex items-center justify-between text-xs">
              <div className="flex items-center gap-2">
                <Shield className="w-4 h-4 text-gray-400" />
                <span className={cn('px-2 py-1 rounded border', getRiskColor(tool.risk))}>
                  {getRiskLabel(tool.risk)}
                </span>
              </div>
              {tool.requiresConfirmation && (
                <div className="flex items-center gap-1 text-yellow-500">
                  <AlertTriangle className="w-4 h-4" />
                  <span>Требует подтверждения</span>
                </div>
              )}
            </div>

            <div className="mt-4 pt-4 border-t border-gray-800 text-xs text-gray-500">
              Использован: {tool.usageCount} раз
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
