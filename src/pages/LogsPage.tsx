import { motion } from 'framer-motion';
import { ScrollText, Trash2 } from 'lucide-react';
import { useAppStore } from '../store';
import { cn } from '../lib/utils';

export function LogsPage() {
  const { logs, clearLogs } = useAppStore();

  const getLevelColor = (level: string) => {
    switch (level) {
      case 'info': return 'text-blue-500';
      case 'warning': return 'text-yellow-500';
      case 'error': return 'text-red-500';
      case 'debug': return 'text-gray-500';
      default: return 'text-gray-500';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">Логи</h1>
          <p className="text-gray-400">Системные события и отладка</p>
        </div>
        <button
          onClick={clearLogs}
          className="px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg transition-colors flex items-center gap-2"
        >
          <Trash2 className="w-4 h-4" />
          Очистить
        </button>
      </motion.div>

      {/* Logs List */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
        <div className="p-4 border-b border-gray-800">
          <div className="flex items-center gap-2">
            <ScrollText className="w-5 h-5 text-gray-400" />
            <span className="text-sm text-gray-400">{logs.length} записей</span>
          </div>
        </div>
        <div className="max-h-[600px] overflow-y-auto">
          {logs.length === 0 ? (
            <div className="p-12 text-center text-gray-500">
              Нет записей в логе
            </div>
          ) : (
            <div className="divide-y divide-gray-800">
              {logs.map((log, index) => (
                <motion.div
                  key={log.id}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: index * 0.02 }}
                  className="p-4 hover:bg-gray-800/50 transition-colors"
                >
                  <div className="flex items-start gap-3">
                    <span className={cn('text-xs font-mono', getLevelColor(log.level))}>
                      [{log.level.toUpperCase()}]
                    </span>
                    <div className="flex-1">
                      <div className="text-sm text-white">{log.message}</div>
                      <div className="text-xs text-gray-500 mt-1">
                        {log.component} • {new Date(log.timestamp).toLocaleString('ru-RU')}
                      </div>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
