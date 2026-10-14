/**
 * API клиент для взаимодействия с backend
 */

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API Error: ${endpoint}`, error);
      throw error;
    }
  }

  // Health check
  async health() {
    return this.request<{ status: string; timestamp: string }>('/api/health');
  }

  // Metrics
  async getMetrics() {
    return this.request<{
      cpu: number;
      ram: number;
      ram_total: number;
      events_published: number;
      events_delivered: number;
      events_failed: number;
      uptime: number;
    }>('/api/metrics');
  }

  // FSM
  async getFsmState() {
    return this.request<{ state: string }>('/api/fsm');
  }

  // Chat
  async sendMessage(message: string, sessionId?: string) {
    return this.request<{
      user_message: any;
      assistant_message: any;
      fsm_state: string;
    }>('/api/chat', {
      method: 'POST',
      body: JSON.stringify({ message, session_id: sessionId }),
    });
  }

  async getMessages() {
    return this.request<{ messages: any[] }>('/api/messages');
  }

  async clearMessages() {
    return this.request<{ status: string }>('/api/messages', {
      method: 'DELETE',
    });
  }

  // Documents
  async getDocuments() {
    return this.request<{ documents: any[] }>('/api/documents');
  }

  async uploadDocument(title: string, content: string, format: string) {
    return this.request<any>('/api/documents', {
      method: 'POST',
      body: JSON.stringify({ title, content, format }),
    });
  }

  async deleteDocument(docId: string) {
    return this.request<{ status: string }>(`/api/documents/${docId}`, {
      method: 'DELETE',
    });
  }

  // Tools
  async getTools() {
    return this.request<{ tools: any[] }>('/api/tools');
  }

  async executeTool(toolId: string, args: any) {
    return this.request<any>(`/api/tools/${toolId}/execute`, {
      method: 'POST',
      body: JSON.stringify({ tool_id: toolId, arguments: args }),
    });
  }

  // Logs
  async getLogs() {
    return this.request<{ logs: any[] }>('/api/logs');
  }

  // Audit
  async getAuditLog() {
    return this.request<{ audit_log: any[] }>('/api/audit');
  }

  // WebSocket
  connectWebSocket(onMessage: (data: any) => void): WebSocket {
    const wsUrl = this.baseUrl.replace('http', 'ws') + '/ws';
    const ws = new WebSocket(wsUrl);

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        onMessage(data);
      } catch (error) {
        console.error('WebSocket message error:', error);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    ws.onclose = () => {
      console.log('WebSocket closed');
    };

    return ws;
  }
}

export const api = new ApiClient();
export default api;
