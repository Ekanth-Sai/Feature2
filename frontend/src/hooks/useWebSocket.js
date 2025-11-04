import { useEffect, useState, useRef, useCallback } from 'react';
import { WEBSOCKET_URL } from '../utils/constants';

export const useWebSocket = (endpoint = '/realtime') => {
  const [data, setData] = useState(null);
  const [connected, setConnected] = useState(false);
  const [error, setError] = useState(null);
  const ws = useRef(null);
  const reconnectTimeout = useRef(null);
  const reconnectAttempts = useRef(0);
  const maxReconnectAttempts = 5;

  const connect = useCallback(() => {
    try {
      const wsUrl = `${WEBSOCKET_URL}${endpoint}`;
      ws.current = new WebSocket(wsUrl);

      ws.current.onopen = () => {
        console.log('WebSocket connected');
        setConnected(true);
        setError(null);
        reconnectAttempts.current = 0;
      };

      ws.current.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          setData(message);
        } catch (err) {
          console.error('Failed to parse WebSocket message:', err);
        }
      };

      ws.current.onerror = (event) => {
        console.error('WebSocket error:', event);
        setError('WebSocket connection error');
      };

      ws.current.onclose = () => {
        console.log('WebSocket disconnected');
        setConnected(false);

        if (reconnectAttempts.current < maxReconnectAttempts) {
          reconnectAttempts.current += 1;
          const delay = Math.min(1000 * Math.pow(2, reconnectAttempts.current), 30000);
          
          reconnectTimeout.current = setTimeout(() => {
            console.log(`Reconnecting... Attempt ${reconnectAttempts.current}`);
            connect();
          }, delay);
        } else {
          setError('Failed to connect after multiple attempts');
        }
      };
    } catch (err) {
      console.error('Failed to create WebSocket:', err);
      setError('Failed to create WebSocket connection');
    }
  }, [endpoint]);

  const disconnect = useCallback(() => {
    if (reconnectTimeout.current) {
      clearTimeout(reconnectTimeout.current);
    }
    if (ws.current) {
      ws.current.close();
      ws.current = null;
    }
  }, []);

  const send = useCallback((message) => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(message));
    } else {
      console.warn('WebSocket is not connected');
    }
  }, []);

  useEffect(() => {
    connect();
    
    return () => {
      disconnect();
    };
  }, [connect, disconnect]);

  return {
    data,
    connected,
    error,
    send,
    reconnect: connect
  };
};

export const useStockSubscription = (symbols = []) => {
  const { data, connected, send } = useWebSocket('/subscribe');
  const [stockData, setStockData] = useState({});

  useEffect(() => {
    if (connected && symbols.length > 0) {
      send({
        action: 'subscribe',
        symbols
      });
    }

    return () => {
      if (connected && symbols.length > 0) {
        send({
          action: 'unsubscribe'
        });
      }
    };
  }, [connected, symbols, send]);

  useEffect(() => {
    if (data && data.type === 'symbol_update') {
      const updates = {};
      data.data.forEach(stock => {
        updates[stock.symbol] = stock;
      });
      setStockData(updates);
    }
  }, [data]);

  return {
    stockData,
    connected
  };
};
