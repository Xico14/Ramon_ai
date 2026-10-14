// FSM состояния ассистента
export type FSMState = 'IDLE' | 'WAKE' | 'LISTEN' | 'THINK' | 'SPEAK' | 'BARGE_IN';

// Роли сообщений
export type MessageRole = 'user' | 'assistant' | 'system';

// Сообщение в чате
export interface Message {
  id: string;
  role: MessageRole;
  content: string;
  timestamp: Date;
  metadata?: {
    latency?: number;
    tokens?: number;
    toolUsed?: string;
  };
}

// Документ для RAG
export interface Document {
  id: string;
  title: string;
  source: string;
  format: 'pdf' | 'txt' | 'md' | 'docx';
  size: number;
  chunks: number;
  uploadedAt: Date;
  content?: string;
}

// Инструмент MCP
export interface Tool {
  id: string;
  name: string;
  description: string;
  scope: string;
  risk: 'low' | 'medium' | 'high';
  requiresConfirmation: boolean;
  enabled: boolean;
  lastUsed?: Date;
  usageCount: number;
}

// Метрики системы
export interface Metrics {
  cpu: number;
  ram: number;
  ramTotal: number;
  eventsPublished: number;
  eventsDelivered: number;
  eventsFailed: number;
  fsmState: FSMState;
  uptime: number;
  latency: {
    stt: number;
    tts: number;
    llm: number;
    rag: number;
  };
}

// Запись в логе
export interface LogEntry {
  id: string;
  timestamp: Date;
  level: 'info' | 'warning' | 'error' | 'debug';
  component: string;
  message: string;
  details?: string;
}

// Запись в аудит-логе
export interface AuditEntry {
  id: string;
  timestamp: Date;
  toolName: string;
  scope: string;
  risk: 'low' | 'medium' | 'high';
  userConfirmed: boolean;
  success: boolean;
  error?: string;
}

// Настройки приложения
export interface Settings {
  // Общие
  theme: 'dark' | 'light' | 'system';
  language: 'ru' | 'en';
  wakeWord: string;
  
  // Голос
  voiceEnabled: boolean;
  voiceSpeed: number;
  voicePitch: number;
  autoListen: boolean;
  
  // LLM
  modelPath: string;
  temperature: number;
  maxTokens: number;
  contextSize: number;
  
  // RAG
  ragEnabled: boolean;
  topK: number;
  chunkSize: number;
  
  // Безопасность
  auditEnabled: boolean;
  confirmDangerousTools: boolean;
  
  // UI
  animationsEnabled: boolean;
  soundEffects: boolean;
  compactMode: boolean;
}

// Состояние подключения к бэкенду
export type ConnectionStatus = 'connected' | 'connecting' | 'disconnected' | 'error';

// Событие от бэкенда
export interface BackendEvent {
  type: string;
  data: any;
  timestamp: number;
}
