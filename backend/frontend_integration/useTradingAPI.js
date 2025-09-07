/**
 * React Hooks for Trading API
 * Custom hooks for easy integration with React applications
 */

import { useState, useEffect, useCallback, useRef } from 'react';

/**
 * Hook for account information
 */
export const useAccountInfo = (apiKey, autoFetch = true) => {
  const [accountInfo, setAccountInfo] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchAccountInfo = useCallback(async () => {
    if (!apiKey) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const api = new TradingAPI(apiKey);
      const result = await api.getAccountInfo();
      setAccountInfo(result.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [apiKey]);

  useEffect(() => {
    if (autoFetch) {
      fetchAccountInfo();
    }
  }, [fetchAccountInfo, autoFetch]);

  return { accountInfo, loading, error, refetch: fetchAccountInfo };
};

/**
 * Hook for account balance
 */
export const useBalance = (apiKey, asset, autoFetch = true) => {
  const [balance, setBalance] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchBalance = useCallback(async () => {
    if (!apiKey || !asset) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const api = new TradingAPI(apiKey);
      const result = await api.getBalance(asset);
      setBalance(result.data.balance);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [apiKey, asset]);

  useEffect(() => {
    if (autoFetch) {
      fetchBalance();
    }
  }, [fetchBalance, autoFetch]);

  return { balance, loading, error, refetch: fetchBalance };
};

/**
 * Hook for open orders
 */
export const useOpenOrders = (apiKey, autoFetch = true) => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchOrders = useCallback(async () => {
    if (!apiKey) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const api = new TradingAPI(apiKey);
      const result = await api.getOpenOrders();
      setOrders(result.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [apiKey]);

  useEffect(() => {
    if (autoFetch) {
      fetchOrders();
    }
  }, [fetchOrders, autoFetch]);

  return { orders, loading, error, refetch: fetchOrders };
};

/**
 * Hook for trading operations
 */
export const useTrading = (apiKey) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const placeBuyOrder = useCallback(async (symbol, quantity) => {
    if (!apiKey) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const api = new TradingAPI(apiKey);
      const result = await api.placeBuyOrder(symbol, quantity);
      return result.data;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [apiKey]);

  const placeSellOrder = useCallback(async (symbol, quantity) => {
    if (!apiKey) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const api = new TradingAPI(apiKey);
      const result = await api.placeSellOrder(symbol, quantity);
      return result.data;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [apiKey]);

  const cancelOrder = useCallback(async (orderId, symbol = 'BTCUSDT') => {
    if (!apiKey) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const api = new TradingAPI(apiKey);
      const result = await api.cancelOrder(orderId, symbol);
      return result.data;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [apiKey]);

  return {
    placeBuyOrder,
    placeSellOrder,
    cancelOrder,
    loading,
    error
  };
};

/**
 * Hook for DEX operations
 */
export const useDEX = (apiKey) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const getQuote = useCallback(async (tokenIn, tokenOut, amount, chainId) => {
    if (!apiKey) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const api = new TradingAPI(apiKey);
      const result = await api.getDEXQuote(tokenIn, tokenOut, amount, chainId);
      return result.data;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [apiKey]);

  const assembleTransaction = useCallback(async (pathId, userAddress) => {
    if (!apiKey) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const api = new TradingAPI(apiKey);
      const result = await api.assembleDEXTransaction(pathId, userAddress);
      return result.data;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [apiKey]);

  return {
    getQuote,
    assembleTransaction,
    loading,
    error
  };
};

/**
 * Hook for WebSocket connection
 */
export const useWebSocket = (apiKey) => {
  const [connected, setConnected] = useState(false);
  const [messages, setMessages] = useState([]);
  const [error, setError] = useState(null);
  const apiRef = useRef(null);

  const connect = useCallback(() => {
    if (!apiKey || apiRef.current) return;
    
    try {
      const api = new TradingAPI(apiKey);
      apiRef.current = api;
      
      api.on('connected', () => {
        setConnected(true);
        setError(null);
      });
      
      api.on('disconnected', () => {
        setConnected(false);
      });
      
      api.on('error', (err) => {
        setError(err);
      });
      
      api.on('message', (data) => {
        setMessages(prev => [...prev, data]);
      });
      
      api.connectWebSocket();
    } catch (err) {
      setError(err.message);
    }
  }, [apiKey]);

  const disconnect = useCallback(() => {
    if (apiRef.current) {
      apiRef.current.disconnectWebSocket();
      apiRef.current = null;
      setConnected(false);
    }
  }, []);

  useEffect(() => {
    return () => {
      disconnect();
    };
  }, [disconnect]);

  return {
    connected,
    messages,
    error,
    connect,
    disconnect
  };
};

/**
 * Hook for system status
 */
export const useSystemStatus = (apiKey, autoFetch = true) => {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchStatus = useCallback(async () => {
    if (!apiKey) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const api = new TradingAPI(apiKey);
      const result = await api.getSystemStatus();
      setStatus(result.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [apiKey]);

  useEffect(() => {
    if (autoFetch) {
      fetchStatus();
    }
  }, [fetchStatus, autoFetch]);

  return { status, loading, error, refetch: fetchStatus };
};

/**
 * Hook for event triggering
 */
export const useEvents = (apiKey) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const triggerEvent = useCallback(async (eventData) => {
    if (!apiKey) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const api = new TradingAPI(apiKey);
      const result = await api.triggerEvent(eventData);
      return result.data;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [apiKey]);

  const triggerTradingEvent = useCallback(async (exchange, quantity, price, pair, side) => {
    const eventData = `|${exchange}|${quantity}|${price}|${pair}|${side}|`;
    return triggerEvent(eventData);
  }, [triggerEvent]);

  return {
    triggerEvent,
    triggerTradingEvent,
    loading,
    error
  };
};
