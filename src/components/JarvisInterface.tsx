import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Mic, MicOff, Send, Volume2, VolumeX, 
  Cpu, HardDrive, Activity, Zap,
  MessageCircle, Settings, Power,
  Brain, Radio, Waves
} from 'lucide-react';

type FSMState = 'IDLE' | 'WAKE' | 'LISTEN' | 'THINK' | 'SPEAK' | 'BARGE_IN';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export default function JarvisInterface() {
  const [fsmState, setFsmState] = useState<FSMState>('IDLE');
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [metrics, setMetrics] = useState({
    cpu: 15,
    ram: 234,
    events: 0,
  });

  // Симуляция метрик
  useEffect(() => {
    const interval = setInterval(() => {
      setMetrics(prev => ({
        cpu: Math.max(5, Math.min(95, prev.cpu + (Math.random() - 0.5) * 10)),
        ram: Math.max(200, Math.min(800, prev.ram + (Math.random() - 0.5) * 20)),
        events: prev.events + Math.floor(Math.random() * 5),
      }));
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  // Симуляция состояний FSM
  useEffect(() => {
    if (fsmState === 'LISTEN') {
      const timer = setTimeout(() => {
        setFsmState('THINK');
        setTimeout(() => {
          setFsmState('SPEAK');
          setTimeout(() => setFsmState('IDLE'), 3000);
        }, 2000);
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [fsmState]);

  const handleSend = () => {
    if (!inputText.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputText,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setFsmState('LISTEN');

    // Симуляция ответа
    setTimeout(() => {
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Я обработал ваш запрос. Чем могу помочь?',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, assistantMessage]);
    }, 2500);
  };

  const handleMicToggle = () => {
    setIsListening(!isListening);
    if (!isListening) {
      setFsmState('WAKE');
      setTimeout(() => setFsmState('LISTEN'), 500);
    }
  };

  const getStateColor = () => {
    switch (fsmState) {
      case 'IDLE': return 'from-gray-500 to-gray-700';
      case 'WAKE': return 'from-yellow-500 to-orange-600';
      case 'LISTEN': return 'from-blue-500 to-cyan-600';
      case 'THINK': return 'from-purple-500 to-pink-600';
      case 'SPEAK': return 'from-green-500 to-emerald-600';
      case 'BARGE_IN': return 'from-red-500 to-rose-600';
      default: return 'from-gray-500 to-gray-700';
    }
  };

  const getStateLabel = () => {
    const labels: Record<FSMState, string> = {
      IDLE: 'Ожидание',
      WAKE: 'Пробуждение',
      LISTEN: 'Слушаю',
      THINK: 'Думаю',
      SPEAK: 'Говорю',
      BARGE_IN: 'Перебит',
    };
    return labels[fsmState];
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-blue-950 to-slate-950 text-white overflow-hidden">
      {/* Animated Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-blue-900/20 via-transparent to-transparent"></div>
        
        {/* Grid Pattern */}
        <div className="absolute inset-0 bg-[linear-gradient(rgba(59,130,246,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(59,130,246,0.03)_1px,transparent_1px)] bg-[size:50px_50px]"></div>
        
        <motion.div
          className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.3, 0.5, 0.3],
          }}
          transition={{
            duration: 8,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />
        <motion.div
          className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl"
          animate={{
            scale: [1.2, 1, 1.2],
            opacity: [0.3, 0.5, 0.3],
          }}
          transition={{
            duration: 8,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />
        <motion.div
          className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-cyan-500/5 rounded-full blur-3xl"
          animate={{
            scale: [1, 1.1, 1],
            rotate: [0, 180, 360],
          }}
          transition={{
            duration: 20,
            repeat: Infinity,
            ease: "linear"
          }}
        />
      </div>

      <div className="relative z-10 container mx-auto px-4 py-8 max-w-7xl">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center justify-between mb-8"
        >
          <div className="flex items-center gap-4">
            <motion.div
              className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/50"
              animate={{
                boxShadow: [
                  '0 0 20px rgba(59, 130, 246, 0.5)',
                  '0 0 40px rgba(147, 51, 234, 0.5)',
                  '0 0 20px rgba(59, 130, 246, 0.5)',
                ]
              }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              <Brain className="w-6 h-6" />
            </motion.div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                ДЖАРВИС
              </h1>
              <p className="text-xs text-gray-400">AI Ассистент v1.0</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button className="p-2 rounded-lg bg-white/5 hover:bg-white/10 transition-colors">
              <Settings className="w-5 h-5" />
            </button>
            <button className="p-2 rounded-lg bg-red-500/20 hover:bg-red-500/30 transition-colors text-red-400">
              <Power className="w-5 h-5" />
            </button>
          </div>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Panel - Avatar & Status */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="lg:col-span-1 space-y-6"
          >
            {/* Avatar */}
            <div className="bg-white/5 backdrop-blur-xl rounded-2xl p-8 border border-white/10">
              <div className="relative">
                {/* Animated Rings */}
                <motion.div
                  className="absolute inset-0 rounded-full"
                  animate={{
                    rotate: 360,
                  }}
                  transition={{
                    duration: 20,
                    repeat: Infinity,
                    ease: "linear"
                  }}
                >
                  <div className="absolute inset-0 rounded-full border-2 border-blue-500/30 border-dashed"></div>
                </motion.div>

                <motion.div
                  className="absolute inset-4 rounded-full"
                  animate={{
                    rotate: -360,
                  }}
                  transition={{
                    duration: 15,
                    repeat: Infinity,
                    ease: "linear"
                  }}
                >
                  <div className="absolute inset-0 rounded-full border-2 border-purple-500/30 border-dashed"></div>
                </motion.div>

                {/* Core Avatar */}
                <motion.div
                  className={`relative w-full aspect-square rounded-full bg-gradient-to-br ${getStateColor()} flex items-center justify-center shadow-2xl`}
                  animate={{
                    scale: fsmState === 'LISTEN' ? [1, 1.05, 1] : 1,
                  }}
                  transition={{
                    duration: 1,
                    repeat: fsmState === 'LISTEN' ? Infinity : 0,
                  }}
                >
                  <AnimatePresence mode="wait">
                    <motion.div
                      key={fsmState}
                      initial={{ scale: 0, opacity: 0 }}
                      animate={{ scale: 1, opacity: 1 }}
                      exit={{ scale: 0, opacity: 0 }}
                      className="text-6xl"
                    >
                      {fsmState === 'IDLE' && '💤'}
                      {fsmState === 'WAKE' && ' 👂'}
                      {fsmState === 'LISTEN' && '🎧'}
                      {fsmState === 'THINK' && '💭'}
                      {fsmState === 'SPEAK' && '🗣️'}
                      {fsmState === 'BARGE_IN' && '🛑'}
                    </motion.div>
                  </AnimatePresence>

                  {/* Sound Waves */}
                  {(fsmState === 'LISTEN' || fsmState === 'SPEAK') && (
                    <motion.div
                      className="absolute inset-0 rounded-full"
                      animate={{
                        scale: [1, 1.5, 1],
                        opacity: [0.5, 0, 0.5],
                      }}
                      transition={{
                        duration: 2,
                        repeat: Infinity,
                      }}
                    >
                      <div className="absolute inset-0 rounded-full border-2 border-current"></div>
                    </motion.div>
                  )}
                </motion.div>
              </div>

              {/* State Label */}
              <motion.div
                className="mt-6 text-center"
                key={fsmState}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <div className={`inline-block px-4 py-2 rounded-full bg-gradient-to-r ${getStateColor()} text-white font-semibold shadow-lg`}>
                  {getStateLabel()}
                </div>
                <div className="mt-3 flex items-center justify-center gap-2 text-xs text-gray-400">
                  <motion.div
                    className="w-2 h-2 rounded-full bg-green-500"
                    animate={{
                      scale: [1, 1.5, 1],
                      opacity: [1, 0.5, 1],
                    }}
                    transition={{
                      duration: 2,
                      repeat: Infinity,
                    }}
                  />
                  <span>Система активна</span>
                </div>
              </motion.div>

              {/* FSM States Visualization */}
              <div className="mt-6">
                <div className="text-xs text-gray-400 mb-2 text-center">Состояния FSM</div>
                <div className="flex items-center justify-center gap-1">
                  {(['IDLE', 'WAKE', 'LISTEN', 'THINK', 'SPEAK'] as FSMState[]).map((state) => (
                    <motion.div
                      key={state}
                      className={`w-8 h-8 rounded-lg flex items-center justify-center text-xs font-bold transition-all ${
                        fsmState === state
                          ? 'bg-gradient-to-br from-blue-500 to-purple-600 text-white scale-110 shadow-lg'
                          : 'bg-white/5 text-gray-500'
                      }`}
                      whileHover={{ scale: 1.1 }}
                    >
                      {state[0]}
                    </motion.div>
                  ))}
                </div>
              </div>
            </div>

            {/* Metrics */}
            <div className="bg-white/5 backdrop-blur-xl rounded-2xl p-6 border border-white/10">
              <h3 className="text-sm font-semibold text-gray-400 mb-4 flex items-center gap-2">
                <Activity className="w-4 h-4" />
                СИСТЕМНЫЕ МЕТРИКИ
              </h3>
              <div className="space-y-4">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs text-gray-400 flex items-center gap-2">
                      <Cpu className="w-3 h-3" />
                      CPU
                    </span>
                    <span className="text-xs font-mono text-blue-400">{metrics.cpu.toFixed(1)}%</span>
                  </div>
                  <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
                    <motion.div
                      className="h-full bg-gradient-to-r from-blue-500 to-cyan-500"
                      animate={{ width: `${metrics.cpu}%` }}
                      transition={{ duration: 0.5 }}
                    />
                  </div>
                </div>

                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs text-gray-400 flex items-center gap-2">
                      <HardDrive className="w-3 h-3" />
                      RAM
                    </span>
                    <span className="text-xs font-mono text-purple-400">{metrics.ram.toFixed(0)} MB</span>
                  </div>
                  <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
                    <motion.div
                      className="h-full bg-gradient-to-r from-purple-500 to-pink-500"
                      animate={{ width: `${(metrics.ram / 800) * 100}%` }}
                      transition={{ duration: 0.5 }}
                    />
                  </div>
                </div>

                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs text-gray-400 flex items-center gap-2">
                      <Zap className="w-3 h-3" />
                      Events
                    </span>
                    <span className="text-xs font-mono text-green-400">{metrics.events}</span>
                  </div>
                  <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
                    <motion.div
                      className="h-full bg-gradient-to-r from-green-500 to-emerald-500"
                      animate={{ width: `${Math.min(100, metrics.events / 2)}%` }}
                      transition={{ duration: 0.5 }}
                    />
                  </div>
                </div>
              </div>
            </div>
          </motion.div>

          {/* Center Panel - Chat */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="lg:col-span-2"
          >
            <div className="bg-white/5 backdrop-blur-xl rounded-2xl border border-white/10 h-[600px] flex flex-col">
              {/* Chat Header */}
              <div className="p-4 border-b border-white/10 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                    <MessageCircle className="w-5 h-5" />
                  </div>
                  <div>
                    <h2 className="font-semibold">Диалог</h2>
                    <p className="text-xs text-gray-400">
                      {messages.length} сообщений
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <motion.div
                    className="w-2 h-2 rounded-full bg-green-500"
                    animate={{
                      scale: [1, 1.5, 1],
                      opacity: [1, 0.5, 1],
                    }}
                    transition={{
                      duration: 2,
                      repeat: Infinity,
                    }}
                  />
                  <span className="text-xs text-gray-400">Online</span>
                </div>
              </div>

              {/* Messages */}
              <div className="flex-1 overflow-y-auto p-4 space-y-4">
                <AnimatePresence>
                  {messages.length === 0 ? (
                    <motion.div
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      className="flex flex-col items-center justify-center h-full text-center"
                    >
                      <motion.div
                        animate={{
                          y: [0, -10, 0],
                        }}
                        transition={{
                          duration: 3,
                          repeat: Infinity,
                        }}
                        className="text-6xl mb-4"
                      >
                        🤖
                      </motion.div>
                      <h3 className="text-xl font-semibold mb-2">Привет! Я Джарвис</h3>
                      <p className="text-gray-400 text-sm max-w-md">
                        Я ваш AI-ассистент. Скажите "Джарвис" или нажмите на микрофон, чтобы начать разговор.
                      </p>
                    </motion.div>
                  ) : (
                    messages.map((message) => (
                      <motion.div
                        key={message.id}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                      >
                        <div
                          className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                            message.role === 'user'
                              ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white'
                              : 'bg-white/10 text-white'
                          }`}
                        >
                          <p className="text-sm">{message.content}</p>
                          <p className="text-xs opacity-60 mt-1">
                            {message.timestamp.toLocaleTimeString('ru-RU', {
                              hour: '2-digit',
                              minute: '2-digit',
                            })}
                          </p>
                        </div>
                      </motion.div>
                    ))
                  )}
                </AnimatePresence>
              </div>

              {/* Voice Visualization */}
              {(isListening || fsmState === 'SPEAK') && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  className="px-4 py-3 border-t border-white/10"
                >
                  <div className="flex items-center justify-center gap-1 h-12">
                    {[...Array(20)].map((_, i) => (
                      <motion.div
                        key={i}
                        className="w-1 bg-gradient-to-t from-blue-500 to-purple-500 rounded-full"
                        animate={{
                          height: [
                            `${20 + Math.random() * 30}%`,
                            `${40 + Math.random() * 40}%`,
                            `${20 + Math.random() * 30}%`,
                          ],
                        }}
                        transition={{
                          duration: 0.5 + Math.random() * 0.5,
                          repeat: Infinity,
                          delay: i * 0.05,
                        }}
                      />
                    ))}
                  </div>
                </motion.div>
              )}

              {/* Input */}
              <div className="p-4 border-t border-white/10">
                <div className="flex items-center gap-3">
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={handleMicToggle}
                    className={`p-3 rounded-full transition-all ${
                      isListening
                        ? 'bg-red-500 shadow-lg shadow-red-500/50'
                        : 'bg-white/10 hover:bg-white/20'
                    }`}
                  >
                    {isListening ? (
                      <MicOff className="w-5 h-5" />
                    ) : (
                      <Mic className="w-5 h-5" />
                    )}
                  </motion.button>

                  <div className="flex-1 relative">
                    <input
                      type="text"
                      value={inputText}
                      onChange={(e) => setInputText(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                      placeholder="Введите сообщение..."
                      className="w-full bg-white/10 rounded-full px-4 py-3 pr-12 text-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500/50"
                    />
                    <motion.button
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.9 }}
                      onClick={handleSend}
                      className="absolute right-2 top-1/2 -translate-y-1/2 p-2 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 transition-all"
                    >
                      <Send className="w-4 h-4" />
                    </motion.button>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        </div>

        {/* Bottom Panel - Quick Actions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="mt-6 grid grid-cols-2 md:grid-cols-4 gap-4"
        >
          {[
            { icon: Radio, label: 'Wake Word', color: 'from-yellow-500 to-orange-600', status: 'Готов' },
            { icon: Waves, label: 'Audio', color: 'from-blue-500 to-cyan-600', status: '16 kHz' },
            { icon: Brain, label: 'LLM', color: 'from-purple-500 to-pink-600', status: 'Qwen2.5' },
            { icon: Activity, label: 'Health', color: 'from-green-500 to-emerald-600', status: 'OK' },
          ].map((item, index) => (
            <motion.button
              key={item.label}
              whileHover={{ scale: 1.05, y: -5 }}
              whileTap={{ scale: 0.95 }}
              className="bg-white/5 backdrop-blur-xl rounded-xl p-4 border border-white/10 hover:border-white/20 transition-all group"
            >
              <div className={`w-10 h-10 rounded-lg bg-gradient-to-br ${item.color} flex items-center justify-center mb-3 group-hover:scale-110 transition-transform`}>
                <item.icon className="w-5 h-5" />
              </div>
              <div className="text-sm font-semibold">{item.label}</div>
              <div className="text-xs text-gray-400 mt-1">{item.status}</div>
            </motion.button>
          ))}
        </motion.div>

        {/* Footer Info */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="mt-8 text-center text-xs text-gray-500"
        >
          <p>🤖 Джарвис AI Assistant • Python • asyncio • llama-cpp • faster-whisper</p>
          <p className="mt-1">Версия 1.0 • Фазы 0-7.5 завершены</p>
        </motion.div>
      </div>
    </div>
  );
}
