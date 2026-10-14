import { useCallback, useEffect } from 'react';
import { useAppStore } from '../store';
import { useVoice } from './useVoice';
import api from '../lib/api';
import type { Message } from '../types';

export function useChat() {
  const { messages, addMessage, fsmState, setFsmState, settings, clearMessages: clearStoreMessages } = useAppStore();
  const { speak, stopSpeaking } = useVoice();

  // Загрузка истории сообщений при монтировании
  useEffect(() => {
    const loadMessages = async () => {
      try {
        const response = await api.getMessages();
        // Если есть сообщения от API, можно добавить их в store
        // Но пока используем локальное хранилище
      } catch (error) {
        console.error('Error loading messages:', error);
      }
    };

    loadMessages();
  }, []);

  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim()) return;

    // Добавляем сообщение пользователя
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: content.trim(),
      timestamp: new Date(),
    };

    addMessage(userMessage);
    setFsmState('THINK');

    try {
      // Отправляем на backend
      const response = await api.sendMessage(content);

      // Добавляем ответ ассистента
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.assistant_message.content,
        timestamp: new Date(),
        metadata: {
          latency: 1500, // Примерная задержка
          tokens: response.assistant_message.content.split(' ').length,
        },
      };

      addMessage(assistantMessage);

      // Обновляем состояние FSM
      setFsmState(response.fsm_state as any);

      // Озвучиваем ответ если включено
      if (settings.voiceEnabled) {
        setFsmState('SPEAK');
        speak(response.assistant_message.content);

        // Возвращаемся в IDLE после озвучивания
        setTimeout(() => {
          setFsmState('IDLE');
        }, response.assistant_message.content.length * 50);
      } else {
        setFsmState('IDLE');
      }
    } catch (error) {
      console.error('Error sending message:', error);

      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Извините, произошла ошибка при обработке вашего запроса.',
        timestamp: new Date(),
      };

      addMessage(errorMessage);
      setFsmState('IDLE');
    }
  }, [addMessage, setFsmState, speak, settings.voiceEnabled]);

  const clearChat = useCallback(async () => {
    stopSpeaking();
    
    try {
      await api.clearMessages();
    } catch (error) {
      console.error('Error clearing messages:', error);
    }
    
    clearStoreMessages();
  }, [stopSpeaking, clearStoreMessages]);

  return {
    messages,
    sendMessage,
    clearChat,
    isProcessing: fsmState === 'THINK' || fsmState === 'SPEAK',
  };
}
