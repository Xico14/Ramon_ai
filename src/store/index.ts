import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { 
  Message, 
  FSMState, 
  Metrics, 
  Document, 
  Tool, 
  LogEntry, 
  AuditEntry, 
  Settings,
  ConnectionStatus 
} from '../types';

interface AppState {
  // Подключение
  connectionStatus: ConnectionStatus;
  setConnectionStatus: (status: ConnectionStatus) => void;
  
  // FSM
  fsmState: FSMState;
  setFsmState: (state: FSMState) => void;
  
  // Чат
  messages: Message[];
  addMessage: (message: Message) => void;
  clearMessages: () => void;
  
  // Голос
  isListening: boolean;
  setIsListening: (listening: boolean) => void;
  isSpeaking: boolean;
  setIsSpeaking: (speaking: boolean) => void;
  
  // Метрики
  metrics: Metrics;
  updateMetrics: (metrics: Partial<Metrics>) => void;
  
  // Документы
  documents: Document[];
  addDocument: (doc: Document) => void;
  removeDocument: (id: string) => void;
  
  // Инструменты
  tools: Tool[];
  updateTool: (id: string, updates: Partial<Tool>) => void;
  
  // Логи
  logs: LogEntry[];
  addLog: (log: LogEntry) => void;
  clearLogs: () => void;
  
  // Аудит
  auditLog: AuditEntry[];
  addAuditEntry: (entry: AuditEntry) => void;
  
  // Настройки
  settings: Settings;
  updateSettings: (updates: Partial<Settings>) => void;
  resetSettings: () => void;
  
  // UI
  sidebarOpen: boolean;
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;
}

const defaultSettings: Settings = {
  theme: 'dark',
  language: 'ru',
  wakeWord: 'джарвис',
  voiceEnabled: true,
  voiceSpeed: 1.0,
  voicePitch: 1.0,
  autoListen: false,
  modelPath: './models/qwen2.5-3b-q4_k_m.gguf',
  temperature: 0.7,
  maxTokens: 512,
  contextSize: 4096,
  ragEnabled: true,
  topK: 5,
  chunkSize: 500,
  auditEnabled: true,
  confirmDangerousTools: true,
  animationsEnabled: true,
  soundEffects: true,
  compactMode: false,
};

const defaultMetrics: Metrics = {
  cpu: 0,
  ram: 0,
  ramTotal: 8192,
  eventsPublished: 0,
  eventsDelivered: 0,
  eventsFailed: 0,
  fsmState: 'IDLE',
  uptime: 0,
  latency: {
    stt: 0,
    tts: 0,
    llm: 0,
    rag: 0,
  },
};

export const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      // Подключение
      connectionStatus: 'disconnected',
      setConnectionStatus: (status) => set({ connectionStatus: status }),
      
      // FSM
      fsmState: 'IDLE',
      setFsmState: (state) => set({ fsmState: state }),
      
      // Чат
      messages: [],
      addMessage: (message) => set((state) => ({ 
        messages: [...state.messages, message] 
      })),
      clearMessages: () => set({ messages: [] }),
      
      // Голос
      isListening: false,
      setIsListening: (listening) => set({ isListening: listening }),
      isSpeaking: false,
      setIsSpeaking: (speaking) => set({ isSpeaking: speaking }),
      
      // Метрики
      metrics: defaultMetrics,
      updateMetrics: (updates) => set((state) => ({ 
        metrics: { ...state.metrics, ...updates } 
      })),
      
      // Документы
      documents: [],
      addDocument: (doc) => set((state) => ({ 
        documents: [...state.documents, doc] 
      })),
      removeDocument: (id) => set((state) => ({ 
        documents: state.documents.filter(d => d.id !== id) 
      })),
      
      // Инструменты
      tools: [
        {
          id: 'calculator',
          name: 'Калькулятор',
          description: 'Математические вычисления',
          scope: 'math',
          risk: 'low',
          requiresConfirmation: false,
          enabled: true,
          usageCount: 0,
        },
        {
          id: 'web_search',
          name: 'Поиск в интернете',
          description: 'Поиск информации в интернете',
          scope: 'web',
          risk: 'low',
          requiresConfirmation: false,
          enabled: true,
          usageCount: 0,
        },
        {
          id: 'read_file',
          name: 'Чтение файла',
          description: 'Чтение содержимого файла',
          scope: 'files.local',
          risk: 'low',
          requiresConfirmation: false,
          enabled: true,
          usageCount: 0,
        },
        {
          id: 'write_file',
          name: 'Запись файла',
          description: 'Запись в файл',
          scope: 'files.local',
          risk: 'medium',
          requiresConfirmation: true,
          enabled: true,
          usageCount: 0,
        },
        {
          id: 'delete_file',
          name: 'Удаление файла',
          description: 'Удаление файла',
          scope: 'files.dangerous',
          risk: 'high',
          requiresConfirmation: true,
          enabled: true,
          usageCount: 0,
        },
        {
          id: 'open_app',
          name: 'Открытие приложения',
          description: 'Открытие приложения',
          scope: 'system.apps',
          risk: 'medium',
          requiresConfirmation: true,
          enabled: true,
          usageCount: 0,
        },
        {
          id: 'system_command',
          name: 'Системная команда',
          description: 'Выполнение системной команды',
          scope: 'system.dangerous',
          risk: 'high',
          requiresConfirmation: true,
          enabled: false,
          usageCount: 0,
        },
        {
          id: 'send_email',
          name: 'Отправка email',
          description: 'Отправка email',
          scope: 'network.email',
          risk: 'high',
          requiresConfirmation: true,
          enabled: false,
          usageCount: 0,
        },
      ],
      updateTool: (id, updates) => set((state) => ({
        tools: state.tools.map(t => t.id === id ? { ...t, ...updates } : t)
      })),
      
      // Логи
      logs: [],
      addLog: (log) => set((state) => ({ 
        logs: [log, ...state.logs].slice(0, 1000) 
      })),
      clearLogs: () => set({ logs: [] }),
      
      // Аудит
      auditLog: [],
      addAuditEntry: (entry) => set((state) => ({ 
        auditLog: [entry, ...state.auditLog].slice(0, 1000) 
      })),
      
      // Настройки
      settings: defaultSettings,
      updateSettings: (updates) => set((state) => ({ 
        settings: { ...state.settings, ...updates } 
      })),
      resetSettings: () => set({ settings: defaultSettings }),
      
      // UI
      sidebarOpen: true,
      toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
      setSidebarOpen: (open) => set({ sidebarOpen: open }),
    }),
    {
      name: 'jarvis-storage',
      partialize: (state) => ({
        settings: state.settings,
        messages: state.messages,
        documents: state.documents,
      }),
    }
  )
);
