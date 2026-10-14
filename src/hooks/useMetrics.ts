import { useEffect, useRef } from 'react';
import { useAppStore } from '../store';
import api from '../lib/api';

export function useMetrics() {
  const { updateMetrics, setConnectionStatus } = useAppStore();
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    // Подключение к WebSocket для real-time обновлений
    const connectWebSocket = () => {
      try {
        wsRef.current = api.connectWebSocket((data) => {
          if (data.type === 'metrics') {
            updateMetrics({
              cpu: data.data.cpu,
              ram: data.data.ram,
              ramTotal: data.data.ram_total,
              eventsPublished: data.data.events_published,
              eventsDelivered: data.data.events_delivered,
              eventsFailed: data.data.events_failed,
              uptime: data.data.uptime,
            });
            setConnectionStatus('connected');
          }
        });

        wsRef.current.onopen = () => {
          console.log('WebSocket connected');
          setConnectionStatus('connected');
        };

        wsRef.current.onerror = () => {
          console.error('WebSocket error');
          setConnectionStatus('error');
        };

        wsRef.current.onclose = () => {
          console.log('WebSocket closed');
          setConnectionStatus('disconnected');
          
          // Попытка переподключения через 5 секунд
          setTimeout(connectWebSocket, 5000);
        };
      } catch (error) {
        console.error('WebSocket connection error:', error);
        setConnectionStatus('error');
      }
    };

    // Первоначальная загрузка метрик
    const loadMetrics = async () => {
      try {
        const metrics = await api.getMetrics();
        updateMetrics({
          cpu: metrics.cpu,
          ram: metrics.ram,
          ramTotal: metrics.ram_total,
          eventsPublished: metrics.events_published,
          eventsDelivered: metrics.events_delivered,
          eventsFailed: metrics.events_failed,
          uptime: metrics.uptime,
        });
        setConnectionStatus('connected');
      } catch (error) {
        console.error('Error loading metrics:', error);
        setConnectionStatus('disconnected');
      }
    };

    loadMetrics();
    connectWebSocket();

    // Очистка при размонтировании
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [updateMetrics, setConnectionStatus]);

  return {
    // Можно добавить дополнительные методы если нужно
  };
}
