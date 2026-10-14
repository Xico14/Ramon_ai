import { motion } from 'framer-motion';
import { Menu, Bell, User } from 'lucide-react';
import { useAppStore } from '../../store';
import { cn } from '../../lib/utils';

export function Header() {
  const { toggleSidebar, metrics, fsmState } = useAppStore();

  const getStateLabel = () => {
    switch (fsmState) {
      case 'IDLE': return 'Ожидание';
      case 'WAKE': return 'Пробуждение';
      case 'LISTEN': return 'Слушаю';
      case 'THINK': return 'Думаю';
      case 'SPEAK': return 'Говорю';
      case 'BARGE_IN': return 'Перебит';
      default: return 'Неизвестно';
    }
  };

  const getStateColor = () => {
    switch (fsmState) {
      case 'IDLE': return 'from-gray-500 to-gray-600';
      case 'WAKE': return 'from-yellow-500 to-orange-600';
      case 'LISTEN': return 'from-blue-500 to-cyan-600';
      case 'THINK': return 'from-purple-500 to-pink-600';
      case 'SPEAK': return 'from-green-500 to-emerald-600';
      case 'BARGE_IN': return 'from-red-500 to-rose-600';
      default: return 'from-gray-500 to-gray-600';
    }
  };

  return (
    <header className="h-16 bg-gray-900 border-b border-gray-800 flex items-center justify-between px-4 lg:px-6">
      {/* Left */}
      <div className="flex items-center gap-4">
        <button
          onClick={toggleSidebar}
          className="p-2 rounded-lg hover:bg-gray-800 text-gray-400 hover:text-white transition-colors"
        >
          <Menu className="w-5 h-5" />
        </button>

        {/* FSM State Badge */}
        <motion.div
          key={fsmState}
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className={cn(
            'px-3 py-1.5 rounded-full bg-gradient-to-r text-white text-xs font-semibold shadow-lg',
            getStateColor()
          )}
        >
          {getStateLabel()}
        </motion.div>
      </div>

      {/* Right */}
      <div className="flex items-center gap-4">
        {/* Metrics */}
        <div className="hidden md:flex items-center gap-4 text-xs text-gray-400">
          <div className="flex items-center gap-2">
            <span>CPU:</span>
            <span className="text-white font-mono">{metrics.cpu.toFixed(1)}%</span>
          </div>
          <div className="flex items-center gap-2">
            <span>RAM:</span>
            <span className="text-white font-mono">{metrics.ram.toFixed(0)} MB</span>
          </div>
        </div>

        {/* Notifications */}
        <button className="p-2 rounded-lg hover:bg-gray-800 text-gray-400 hover:text-white transition-colors relative">
          <Bell className="w-5 h-5" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full" />
        </button>

        {/* User */}
        <button className="p-2 rounded-lg hover:bg-gray-800 text-gray-400 hover:text-white transition-colors">
          <User className="w-5 h-5" />
        </button>
      </div>
    </header>
  );
}
