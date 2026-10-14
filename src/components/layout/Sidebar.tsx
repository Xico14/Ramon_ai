import { NavLink } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  MessageSquare, 
  LayoutDashboard, 
  FileText, 
  Wrench, 
  Settings, 
  ScrollText,
  Shield,
  X,
  Brain
} from 'lucide-react';
import { cn } from '../../lib/utils';
import { useAppStore } from '../../store';

const navigation = [
  { name: 'Дашборд', href: '/', icon: LayoutDashboard },
  { name: 'Чат', href: '/chat', icon: MessageSquare },
  { name: 'Документы', href: '/documents', icon: FileText },
  { name: 'Инструменты', href: '/tools', icon: Wrench },
  { name: 'Безопасность', href: '/security', icon: Shield },
  { name: 'Логи', href: '/logs', icon: ScrollText },
  { name: 'Настройки', href: '/settings', icon: Settings },
];

export function Sidebar() {
  const { sidebarOpen, setSidebarOpen, fsmState, connectionStatus } = useAppStore();

  const getStateColor = () => {
    switch (fsmState) {
      case 'IDLE': return 'bg-gray-500';
      case 'WAKE': return 'bg-yellow-500';
      case 'LISTEN': return 'bg-blue-500';
      case 'THINK': return 'bg-purple-500';
      case 'SPEAK': return 'bg-green-500';
      case 'BARGE_IN': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  const getConnectionColor = () => {
    switch (connectionStatus) {
      case 'connected': return 'bg-green-500';
      case 'connecting': return 'bg-yellow-500';
      case 'disconnected': return 'bg-gray-500';
      case 'error': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  return (
    <>
      {/* Overlay для мобильных */}
      {sidebarOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={() => setSidebarOpen(false)}
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
        />
      )}

      {/* Sidebar */}
      <motion.aside
        initial={false}
        animate={{
          x: sidebarOpen ? 0 : -280,
        }}
        transition={{ type: 'spring', damping: 20, stiffness: 200 }}
        className={cn(
          'fixed left-0 top-0 h-full w-64 bg-gray-900 border-r border-gray-800 z-50',
          'flex flex-col'
        )}
      >
        {/* Logo */}
        <div className="flex items-center justify-between p-4 border-b border-gray-800">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-lg font-bold text-white">Джарвис</h1>
              <p className="text-xs text-gray-400">AI Ассистент</p>
            </div>
          </div>
          <button
            onClick={() => setSidebarOpen(false)}
            className="lg:hidden p-1 rounded-lg hover:bg-gray-800 text-gray-400"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
          {navigation.map((item) => (
            <NavLink
              key={item.name}
              to={item.href}
              onClick={() => setSidebarOpen(false)}
              className={({ isActive }) =>
                cn(
                  'flex items-center gap-3 px-3 py-2 rounded-lg transition-colors',
                  isActive
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-400 hover:bg-gray-800 hover:text-white'
                )
              }
            >
              <item.icon className="w-5 h-5" />
              <span className="text-sm font-medium">{item.name}</span>
            </NavLink>
          ))}
        </nav>

        {/* Status */}
        <div className="p-4 border-t border-gray-800 space-y-3">
          {/* FSM State */}
          <div className="flex items-center gap-2">
            <div className={cn('w-2 h-2 rounded-full', getStateColor())} />
            <span className="text-xs text-gray-400">Состояние:</span>
            <span className="text-xs text-white font-medium">{fsmState}</span>
          </div>

          {/* Connection */}
          <div className="flex items-center gap-2">
            <div className={cn('w-2 h-2 rounded-full', getConnectionColor())} />
            <span className="text-xs text-gray-400">Статус:</span>
            <span className="text-xs text-white font-medium">
              {connectionStatus === 'connected' ? 'Подключено' :
               connectionStatus === 'connecting' ? 'Подключение...' :
               connectionStatus === 'disconnected' ? 'Отключено' : 'Ошибка'}
            </span>
          </div>
        </div>
      </motion.aside>
    </>
  );
}
