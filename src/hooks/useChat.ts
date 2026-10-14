import { useCallback } from 'react';
import { useAppStore } from '../store';
import { useVoice } from './useVoice';
import type { Message } from '../types';

// Простой mock LLM для демонстрации
async function mockLLMResponse(userMessage: string, history: Message[]): Promise<string> {
  // Имитация задержки
  await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000));
  
  const lowerMessage = userMessage.toLowerCase();
  
  // Простые паттерны для ответов
  if (lowerMessage.includes('привет') || lowerMessage.includes('здравствуй')) {
    return 'Привет! Я Джарвис, ваш AI-ассистент. Чем могу помочь?';
  }
  
  if (lowerMessage.includes('как дела') || lowerMessage.includes('как ты')) {
    return 'У меня всё отлично, спасибо! Все системы работают нормально. А у вас?';
  }
  
  if (lowerMessage.includes('что ты умеешь') || lowerMessage.includes('возможности')) {
    return 'Я умею:\n- Отвечать на вопросы\n- Искать информацию в документах\n- Выполнять математические вычисления\n- Управлять файлами\n- Отвечать на голосовые команды\n\nПопробуйте спросить что-нибудь!';
  }
  
  if (lowerMessage.includes('время') || lowerMessage.includes('который час')) {
    const now = new Date();
    return `Сейчас ${now.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })}`;
  }
  
  if (lowerMessage.includes('дата') || lowerMessage.includes('какой день') || lowerMessage.includes('сегодня')) {
    const now = new Date();
    return `Сегодня ${now.toLocaleDateString('ru-RU', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}`;
  }
  
  if (lowerMessage.includes('посчитай') || lowerMessage.includes('сколько будет')) {
    // Попытка извлечь математическое выражение
    const match = userMessage.match(/(\d+)\s*([+\-*/])\s*(\d+)/);
    if (match) {
      const num1 = parseFloat(match[1]);
      const operator = match[2];
      const num2 = parseFloat(match[3]);
      let result = 0;
      
      switch (operator) {
        case '+': result = num1 + num2; break;
        case '-': result = num1 - num2; break;
        case '*': result = num1 * num2; break;
        case '/': result = num2 !== 0 ? num1 / num2 : 0; break;
      }
      
      return `${num1} ${operator} ${num2} = ${result}`;
    }
    return 'Извините, не смог распознать математическое выражение. Попробуйте формат: "посчитай 2 + 2"';
  }
  
  if (lowerMessage.includes('документ') || lowerMessage.includes('файл')) {
    return 'Для работы с документами перейдите на вкладку "Документы". Вы можете загрузить PDF, TXT, MD или DOCX файлы, и я буду искать в них ответы на ваши вопросы.';
  }
  
  if (lowerMessage.includes('инструмент') || lowerMessage.includes('команда')) {
    return 'У меня есть несколько инструментов:\n- Калькулятор\n- Поиск в интернете\n- Чтение файлов\n- Запись файлов\n\nПерейдите на вкладку "Инструменты" для управления ими.';
  }
  
  if (lowerMessage.includes('настройки') || lowerMessage.includes('параметры')) {
    return 'Вы можете настроить меня на вкладке "Настройки". Там можно изменить:\n- Голос и язык\n- Параметры LLM\n- Настройки RAG\n- Безопасность\n- Интерфейс';
  }
  
  if (lowerMessage.includes('пока') || lowerMessage.includes('до свидания') || lowerMessage.includes('выход')) {
    return 'До свидания! Был рад помочь. Возвращайтесь, если понадоблюсь!';
  }
  
  // Дефолтный ответ
  const responses = [
    'Интересный вопрос! Давайте разберёмся вместе.',
    'Понял вас. Позвольте подумать...',
    'Хороший вопрос! Вот что я могу сказать по этому поводу.',
    'Спасибо за вопрос! Я обработал вашу просьбу.',
    'Принято. Вот мой ответ на ваш вопрос.',
  ];
  
  return responses[Math.floor(Math.random() * responses.length)] + 
    '\n\nК сожалению, моя демо-версия имеет ограниченные возможности. В полной версии я использую нейросеть Qwen2.5-3B для генерации ответов и могу искать информацию в ваших документах.';
}

export function useChat() {
  const { messages, addMessage, fsmState, setFsmState, settings } = useAppStore();
  const { speak, stopSpeaking } = useVoice();
  
  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim()) return;
    
    // Добавить сообщение пользователя
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: content.trim(),
      timestamp: new Date(),
    };
    
    addMessage(userMessage);
    
    // Изменить состояние FSM
    setFsmState('THINK');
    
    try {
      // Получить ответ от LLM
      const response = await mockLLMResponse(content, messages);
      
      // Добавить ответ ассистента
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response,
        timestamp: new Date(),
        metadata: {
          latency: 1000 + Math.random() * 2000,
          tokens: response.split(' ').length,
        },
      };
      
      addMessage(assistantMessage);
      
      // Озвучить ответ если включено
      if (settings.voiceEnabled) {
        setFsmState('SPEAK');
        speak(response);
        
        // Вернуться в IDLE после озвучивания
        setTimeout(() => {
          setFsmState('IDLE');
        }, response.length * 50); // Примерное время озвучивания
      } else {
        setFsmState('IDLE');
      }
      
    } catch (error) {
      console.error('Error getting LLM response:', error);
      
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Извините, произошла ошибка при обработке вашего запроса.',
        timestamp: new Date(),
      };
      
      addMessage(errorMessage);
      setFsmState('IDLE');
    }
  }, [messages, addMessage, setFsmState, speak, settings.voiceEnabled]);
  
  const clearChat = useCallback(() => {
    stopSpeaking();
    useAppStore.getState().clearMessages();
  }, [stopSpeaking]);
  
  return {
    messages,
    sendMessage,
    clearChat,
    isProcessing: fsmState === 'THINK' || fsmState === 'SPEAK',
  };
}
