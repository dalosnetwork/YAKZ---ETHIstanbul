/**
 * Trading System JavaScript SDK
 * Frontend integration for cryptocurrency trading system
 */

class TradingAPI {
  constructor(apiKey, baseURL = 'http://localhost:8000') {
    this.apiKey = apiKey;
    this.baseURL = baseURL;
    this.wsConnection = null;
    this.wsCallbacks = new Map();
  }

  /**
   * Make HTTP request to API
   */
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': this.apiKey,
        ...options.headers
      },
      ...options
    };

    if (options.body) {
      config.body = JSON.stringify(options.body);
    }

    try {
      const response = await fetch(url, config);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error?.message || `HTTP ${response.status}`);
      }

      return data;
    } catch (error) {
      console.error(`API request failed: ${endpoint}`, error);
      throw error;
    }
  }

  // ==================== ACCOUNT ENDPOINTS ====================

  /**
   * Get account information
   */
  async getAccountInfo() {
    return this.request('/api/account/info');
  }

  /**
   * Get balance for specific asset
   */
  async getBalance(asset) {
    return this.request(`/api/account/balance/${asset}`);
  }

  // ==================== MARKET DATA ENDPOINTS ====================

  /**
   * Get symbol information
   */
  async getSymbolInfo(symbol) {
    return this.request(`/api/market/symbol/${symbol}`);
  }

  /**
   * Get open orders
   */
  async getOpenOrders() {
    return this.request('/api/orders/open');
  }

  // ==================== TRADING ENDPOINTS ====================

  /**
   * Place market buy order
   */
  async placeBuyOrder(symbol, quantity) {
    return this.request('/api/orders/buy/market', {
      method: 'POST',
      body: { symbol, quantity }
    });
  }

  /**
   * Place market sell order
   */
  async placeSellOrder(symbol, quantity) {
    return this.request('/api/orders/sell/market', {
      method: 'POST',
      body: { symbol, quantity }
    });
  }

  /**
   * Cancel order
   */
  async cancelOrder(orderId, symbol = 'BTCUSDT') {
    return this.request(`/api/orders/${orderId}?symbol=${symbol}`, {
      method: 'DELETE'
    });
  }

  // ==================== DEX ENDPOINTS ====================

  /**
   * Get DEX quote
   */
  async getDEXQuote(tokenIn, tokenOut, amount, chainId) {
    return this.request('/api/dex/quote', {
      method: 'POST',
      body: { tokenIn, tokenOut, amount, chainId }
    });
  }

  /**
   * Assemble DEX transaction
   */
  async assembleDEXTransaction(pathId, userAddress) {
    return this.request('/api/dex/assemble', {
      method: 'POST',
      body: { pathId, userAddress }
    });
  }

  // ==================== EVENT ENDPOINTS ====================

  /**
   * Trigger trading event
   */
  async triggerEvent(eventData) {
    return this.request('/api/events/trigger', {
      method: 'POST',
      body: { event_data: eventData }
    });
  }

  // ==================== SYSTEM ENDPOINTS ====================

  /**
   * Health check
   */
  async healthCheck() {
    return this.request('/api/health');
  }

  /**
   * Get system status
   */
  async getSystemStatus() {
    return this.request('/api/status');
  }

  // ==================== WEBSOCKET CONNECTION ====================

  /**
   * Connect to WebSocket
   */
  connectWebSocket() {
    if (this.wsConnection) {
      return this.wsConnection;
    }

    const wsUrl = this.baseURL.replace('http', 'ws') + '/ws';
    this.wsConnection = new WebSocket(wsUrl);

    this.wsConnection.onopen = () => {
      console.log('WebSocket connected');
      this.emit('connected');
    };

    this.wsConnection.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        this.emit('message', data);
      } catch (error) {
        console.error('WebSocket message parse error:', error);
      }
    };

    this.wsConnection.onclose = () => {
      console.log('WebSocket disconnected');
      this.emit('disconnected');
      this.wsConnection = null;
    };

    this.wsConnection.onerror = (error) => {
      console.error('WebSocket error:', error);
      this.emit('error', error);
    };

    return this.wsConnection;
  }

  /**
   * Disconnect WebSocket
   */
  disconnectWebSocket() {
    if (this.wsConnection) {
      this.wsConnection.close();
      this.wsConnection = null;
    }
  }

  // ==================== EVENT SYSTEM ====================

  /**
   * Add event listener
   */
  on(event, callback) {
    if (!this.wsCallbacks.has(event)) {
      this.wsCallbacks.set(event, []);
    }
    this.wsCallbacks.get(event).push(callback);
  }

  /**
   * Remove event listener
   */
  off(event, callback) {
    if (this.wsCallbacks.has(event)) {
      const callbacks = this.wsCallbacks.get(event);
      const index = callbacks.indexOf(callback);
      if (index > -1) {
        callbacks.splice(index, 1);
      }
    }
  }

  /**
   * Emit event
   */
  emit(event, data) {
    if (this.wsCallbacks.has(event)) {
      this.wsCallbacks.get(event).forEach(callback => {
        try {
          callback(data);
        } catch (error) {
          console.error('Event callback error:', error);
        }
      });
    }
  }

  // ==================== UTILITY METHODS ====================

  /**
   * Format trading event data
   */
  formatTradingEvent(exchange, quantity, price, pair, side) {
    return `|${exchange}|${quantity}|${price}|${pair}|${side}|`;
  }

  /**
   * Parse trading event data
   */
  parseTradingEvent(eventData) {
    const parts = eventData.split('|');
    if (parts.length !== 6) {
      throw new Error('Invalid event format');
    }

    return {
      exchange: parts[1],
      quantity: parseFloat(parts[2]),
      price: parseFloat(parts[3]),
      pair: parts[4],
      side: parts[5]
    };
  }

  /**
   * Get supported chains
   */
  getSupportedChains() {
    return {
      1: 'Ethereum Mainnet',
      137: 'Polygon',
      42161: 'Arbitrum',
      10: 'Optimism',
      8453: 'Base'
    };
  }

  /**
   * Get token addresses for chain
   */
  getTokenAddresses(chainId) {
    const addresses = {
      8453: { // Base
        WETH: '0x4200000000000000000000000000000000000006',
        USDC: '0x833589fcd6edb6e08f4c7c32d4f71b54bda02913',
        USDT: '0x833589fcd6edb6e08f4c7c32d4f71b54bda02913',
        DAI: '0x833589fcd6edb6e08f4c7c32d4f71b54bda02913'
      },
      1: { // Ethereum
        WETH: '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
        USDC: '0xA0b86a33E6441b8c4C8C0e4b8b8b8b8b8b8b8b8b',
        USDT: '0xdAC17F958D2ee523a2206206994597C13D831ec7',
        DAI: '0x6B175474E89094C44Da98b954EedeAC495271d0F'
      }
    };

    return addresses[chainId] || {};
  }
}

// Export for different module systems
if (typeof module !== 'undefined' && module.exports) {
  module.exports = TradingAPI;
} else if (typeof define === 'function' && define.amd) {
  define([], () => TradingAPI);
} else {
  window.TradingAPI = TradingAPI;
}
