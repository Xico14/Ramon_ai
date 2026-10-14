import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { 
  MessageSquare, 
  FileText, 
  Wrench, 
  Activity,
  Cpu,
  HardDrive,
  Zap,
  TrendingUp,
  Clock,
  CheckCircle2
} from 'lucide-react';
import { useAppStore } from '../store';
import { cn } from '../lib/utils';

export function DashboardPage() {
  const navigate = useNavigate();
  const { metrics, messages, documents, tools, fsmState } = useAppStore();

  const stats = [
    {
      title: 'Сообщения',
      value: messages.length,
      icon: MessageSquare,
      color: 'from-blue-500 to-cyan-600',
      href: '/chat',
    },
    {
      title: 'Документы',
      value: documents.length,
      icon: FileText,
      color: 'from-purple-500 to-pink-600',
      href: '/documents',
    },
    {
      title: 'Инструменты',
      value: tools.filter((t: any) => t.enabled).length,
      icon: Wrench,
      color: 'from-green-500 to-emerald-600',
      href: '/tools',
    },
    {
      title: 'События',
      value: metrics.eventsPublished,
      icon: Zap,
      color: 'from-yellow-500 to-orange-600',
      href: '/logs',
    },
  ];

  const systemMetrics = [
    {
      label: 'CPU',
      value: `${metrics.cpu.toFixed(1)}%`,
      percent: metrics.cpu,
      icon: Cpu,
      color: 'from-blue-500 to-cyan-500',
    },
    {
      label: 'RAM',
      value: `${metrics.ram.toFixed(0)} MB`,
      percent: (metrics.ram / metrics.ramTotal) * 100,
      icon: HardDrive,
      color: 'from-purple-500 to-pink-500',
    },
    {
      label: 'События',
      value: metrics.eventsDelivered.toString(),
      percent: Math.min(100, metrics.eventsDelivered / 10),
      icon: Activity,
      color: 'from-green-500 to-emerald-500',
    },
  ];

  const recentActivity = [
    { icon: CheckCircle2, text: 'Система запущена', time: '2 мин назад', color: 'text-green-500' },
    { icon: MessageSquare, text: 'Последнее сообщение', time: '5 мин назад', color: 'text-blue-500' },
    { icon: FileText, text: 'Документ загружен', time: '1 час назад', color: 'text-purple-500' },
    { icon: Wrench, text: 'Инструмент использован', time: '2 часа назад', color: 'text-yellow-500' },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-3xl font-bold text-white mb-2">Дашборд</h1>
        <p className="text-gray-400">Обзор системы и статистика</p>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat, index) => (
          <motion.div
            key={stat.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            onClick={() => navigate(stat.href)}
            className="bg-gray-900 border border-gray-800 rounded-xl p-6 hover:border-gray-700 transition-all cursor-pointer group"
          >
            <div className="flex items-start justify-between mb-4">
              <div className={cn(
                'w-12 h-12 rounded-lg bg-gradient-to-br flex items-center justify-center group-hover:scale-110 transition-transform',
                stat.color
              )}>
                <stat.icon className="w-6 h-6 text-white" />
              </div>
              <TrendingUp className="w-5 h-5 text-green-500" />
            </div>
            <div className="text-3xl font-bold text-white mb-1">{stat.value}</div>
            <div className="text-sm text-gray-400">{stat.title}</div>
          </motion.div>
        ))}
      </div>

      {/* System Metrics */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="bg-gray-900 border border-gray-800 rounded-xl p-6"
      >
        <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
          <Activity className="w-5 h-5" />
          Системные метрики
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {systemMetrics.map((metric) => (
            <div key={metric.label}>
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <metric.icon className="w-4 h-4 text-gray-400" />
                  <span className="text-sm text-gray-400">{metric.label}</span>
                </div>
                <span className="text-sm font-mono text-white">{metric.value}</span>
              </div>
              <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
                <motion.div
                  className={cn('h-full bg-gradient-to-r rounded-full', metric.color)}
                  initial={{ width: 0 }}
                  animate={{ width: `${metric.percent}%` }}
                  transition={{ duration: 1, ease: 'easeOut' }}
                />
              </div>
            </div>
          ))}
        </div>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Activity */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.5 }}
          className="bg-gray-900 border border-gray-800 rounded-xl p-6"
        >
          <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
            <Clock className="w-5 h-5" />
            Последняя активность
          </h2>
          <div className="space-y-4">
            {recentActivity.map((activity, index) => (
              <div key={index} className="flex items-start gap-3">
                <activity.icon className={cn('w-5 h-5 mt-0.5', activity.color)} />
                <div className="flex-1">
                  <div className="text-sm text-white">{activity.text}</div>
                  <div className="text-xs text-gray-500">{activity.time}</div>
                </div>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Quick Actions */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.6 }}
          className="bg-gray-900 border border-gray-800 rounded-xl p-6"
        >
          <h2 className="text-xl font-bold text-white mb-6">Быстрые действия</h2>
          <div className="grid grid-cols-2 gap-3">
            <button
              onClick={() => navigate('/chat')}
              className="p-4 bg-gray-800 hover:bg-gray-700 rounded-lg transition-colors text-left"
            >
              <MessageSquare className="w-6 h-6 text-blue-500 mb-2" />
              <div className="text-sm font-medium text-white">Новый чат</div>
              <div className="text-xs text-gray-400">Начать диалог</div>
            </button>
            <button
              onClick={() => navigate('/documents')}
              className="p-4 bg-gray-800 hover:bg-gray-700 rounded-lg transition-colors text-left"
            >
              <FileText className="w-6 h-6 text-purple-500 mb-2" />
              <div className="text-sm font-medium text-white">Загрузить</div>
              <div className="text-xs text-gray-400">Добавить документ</div>
            </button>
            <button
              onClick={() => navigate('/tools')}
              className="p-4 bg-gray-800 hover:bg-gray-700 rounded-lg transition-colors text-left"
            >
              <Wrench className="w-6 h-6 text-green-500 mb-2" />
              <div className="text-sm font-medium text-white">Инструменты</div>
              <div className="text-xs text-gray-400">Управление</div>
            </button>
            <button
              onClick={() => navigate('/settings')}
              className="p-4 bg-gray-800 hover:bg-gray-700 rounded-lg transition-colors text-left"
            >
              <Activity className="w-6 h-6 text-yellow-500 mb-2" />
              <div className="text-sm font-medium text-white">Настройки</div>
              <div className="text-xs text-gray-400">Конфигурация</div>
            </button>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
