import { motion } from 'framer-motion';
import { Shield, CheckCircle2, XCircle, AlertTriangle } from 'lucide-react';
import { useAppStore } from '../store';
import { cn } from '../lib/utils';

export function SecurityPage() {
  const { auditLog } = useAppStore();

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'low': return 'text-green-500';
      case 'medium': return 'text-yellow-500';
      case 'high': return 'text-red-500';
      default: return 'text-gray-500';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-3xl font-bold text-white mb-2">Безопасность</h1>
        <p className="text-gray-400">Аудит действий и контроль доступа</p>
      </motion.div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-gray-900 border border-gray-800 rounded-xl p-6"
        >
          <div className="flex items-center gap-3 mb-2">
            <CheckCircle2 className="w-8 h-8 text-green-500" />
            <div>
              <div className="text-2xl font-bold text-white">
                {auditLog.filter(e => e.success).length}
              </div>
              <div className="text-sm text-gray-400">Успешных</div>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-gray-900 border border-gray-800 rounded-xl p-6"
        >
          <div className="flex items-center gap-3 mb-2">
            <XCircle className="w-8 h-8 text-red-500" />
            <div>
              <div className="text-2xl font-bold text-white">
                {auditLog.filter(e => !e.success).length}
              </div>
              <div className="text-sm text-gray-400">Неудачных</div>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-gray-900 border border-gray-800 rounded-xl p-6"
        >
          <div className="flex items-center gap-3 mb-2">
            <AlertTriangle className="w-8 h-8 text-yellow-500" />
            <div>
              <div className="text-2xl font-bold text-white">
                {auditLog.filter(e => e.risk === 'high').length}
              </div>
              <div className="text-sm text-gray-400">Высокий риск</div>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Audit Log */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden"
      >
        <div className="p-4 border-b border-gray-800 flex items-center gap-2">
          <Shield className="w-5 h-5 text-gray-400" />
          <span className="text-sm font-semibold text-white">Аудит-лог</span>
        </div>
        <div className="max-h-[500px] overflow-y-auto">
          {auditLog.length === 0 ? (
            <div className="p-12 text-center text-gray-500">
              Нет записей в аудит-логе
            </div>
          ) : (
            <div className="divide-y divide-gray-800">
              {auditLog.map((entry, index) => (
                <motion.div
                  key={entry.id}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: index * 0.02 }}
                  className="p-4 hover:bg-gray-800/50 transition-colors"
                >
                  <div className="flex items-start gap-3">
                    {entry.success ? (
                      <CheckCircle2 className="w-5 h-5 text-green-500 mt-0.5" />
                    ) : (
                      <XCircle className="w-5 h-5 text-red-500 mt-0.5" />
                    )}
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-sm font-medium text-white">{entry.toolName}</span>
                        <span className={cn('text-xs', getRiskColor(entry.risk))}>
                          [{entry.risk}]
                        </span>
                      </div>
                      <div className="text-xs text-gray-400">
                        {entry.scope} • {new Date(entry.timestamp).toLocaleString('ru-RU')}
                      </div>
                      {entry.error && (
                        <div className="text-xs text-red-400 mt-1">{entry.error}</div>
                      )}
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </div>
      </motion.div>
    </div>
  );
}
