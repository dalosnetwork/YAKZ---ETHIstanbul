# 🚀 Trading System API Endpoints

Bu dokümantasyon, frontend'in trading sistemi ile entegrasyonu için gerekli tüm API endpoint'lerini içerir.

## 📋 Genel Bilgiler

- **Base URL**: `http://localhost:8000` (veya production URL'iniz)
- **Content-Type**: `application/json`
- **Authentication**: API Key (header: `X-API-Key`)

## 🔐 Authentication

Tüm endpoint'ler API key ile korunmuştur:

```http
X-API-Key: your_api_key_here
```

## 📊 Market Data Endpoints

### 1. Get Account Info
```http
GET /api/account/info
```

**Response:**
```json
{
  "success": true,
  "data": {
    "accountType": "SPOT",
    "canTrade": true,
    "canWithdraw": true,
    "canDeposit": true,
    "balances": [
      {
        "asset": "USDT",
        "free": "1000.00",
        "locked": "0.00"
      },
      {
        "asset": "BTC",
        "free": "0.001",
        "locked": "0.00"
      }
    ]
  }
}
```

### 2. Get Balance
```http
GET /api/account/balance/{asset}
```

**Parameters:**
- `asset` (string): Asset symbol (e.g., "USDT", "BTC")

**Response:**
```json
{
  "success": true,
  "data": {
    "asset": "USDT",
    "balance": 1000.00
  }
}
```

### 3. Get Symbol Info
```http
GET /api/market/symbol/{symbol}
```

**Parameters:**
- `symbol` (string): Trading pair (e.g., "BTCUSDT", "ETHUSDT")

**Response:**
```json
{
  "success": true,
  "data": {
    "symbol": "BTCUSDT",
    "status": "TRADING",
    "baseAsset": "BTC",
    "quoteAsset": "USDT",
    "filters": {
      "minQty": "0.00001",
      "maxQty": "9000.00000000",
      "stepSize": "0.00001",
      "minPrice": "0.01",
      "maxPrice": "1000000.00",
      "tickSize": "0.01"
    }
  }
}
```

### 4. Get Open Orders
```http
GET /api/orders/open
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "orderId": 12345,
      "symbol": "BTCUSDT",
      "side": "BUY",
      "type": "MARKET",
      "quantity": "0.001",
      "price": "50000.00",
      "status": "NEW",
      "time": 1640995200000
    }
  ]
}
```

## 🛒 Trading Endpoints

### 5. Place Market Buy Order
```http
POST /api/orders/buy/market
```

**Request Body:**
```json
{
  "symbol": "BTCUSDT",
  "quantity": 0.001
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "orderId": 12345,
    "symbol": "BTCUSDT",
    "side": "BUY",
    "type": "MARKET",
    "quantity": "0.001",
    "status": "FILLED",
    "fills": [
      {
        "price": "50000.00",
        "qty": "0.001",
        "commission": "0.000001"
      }
    ]
  }
}
```

### 6. Place Market Sell Order
```http
POST /api/orders/sell/market
```

**Request Body:**
```json
{
  "symbol": "BTCUSDT",
  "quantity": 0.001
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "orderId": 12346,
    "symbol": "BTCUSDT",
    "side": "SELL",
    "type": "MARKET",
    "quantity": "0.001",
    "status": "FILLED"
  }
}
```

### 7. Cancel Order
```http
DELETE /api/orders/{orderId}
```

**Parameters:**
- `orderId` (integer): Order ID to cancel

**Response:**
```json
{
  "success": true,
  "data": {
    "orderId": 12345,
    "status": "CANCELED"
  }
}
```

## 🦄 DEX Trading Endpoints

### 8. Get DEX Quote
```http
POST /api/dex/quote
```

**Request Body:**
```json
{
  "tokenIn": "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",
  "tokenOut": "0x4200000000000000000000000000000000000006",
  "amount": "1000000000000000",
  "chainId": 8453
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "pathId": "47b7611f86b818498d57d53e32093b18",
    "inValues": ["1000.0"],
    "outValues": ["0.001"],
    "gasEstimate": 212756,
    "priceImpact": 0.0,
    "slippageLimitPercent": 1.0
  }
}
```

### 9. Assemble DEX Transaction
```http
POST /api/dex/assemble
```

**Request Body:**
```json
{
  "pathId": "47b7611f86b818498d57d53e32093b18",
  "userAddress": "0x742d35Cc6634C0532925a3b8D0C0C4C2C2C2C2C2"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "transaction": {
      "to": "0x19cEeAd7105607Cd444F5ad10dd51356436095a1",
      "value": "0",
      "data": "0x83bd37f9...",
      "gas": 212756,
      "gasPrice": 1254827
    },
    "simulation": {
      "isSuccess": true,
      "amountsOut": ["0.001"]
    }
  }
}
```

## 📡 WebSocket Endpoints

### 10. WebSocket Connection
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

// Subscribe to market data
ws.send(JSON.stringify({
  "method": "SUBSCRIBE",
  "params": ["btcusdt@ticker", "ethusdt@ticker"],
  "id": 1
}));

// Listen for messages
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Market data:', data);
};
```

## 🔧 System Status Endpoints

### 11. Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "timestamp": 1640995200000,
    "services": {
      "binance": "connected",
      "odos": "connected",
      "contract_listener": "running"
    }
  }
}
```

### 12. Get System Status
```http
GET /api/status
```

**Response:**
```json
{
  "success": true,
  "data": {
    "trading_enabled": true,
    "testnet_mode": true,
    "supported_chains": [1, 137, 42161, 10, 8453],
    "supported_tokens": {
      "8453": ["WETH", "USDC", "USDT", "DAI"]
    }
  }
}
```

## 📝 Error Responses

Tüm endpoint'ler aynı error formatını kullanır:

```json
{
  "success": false,
  "error": {
    "code": "INVALID_SYMBOL",
    "message": "Symbol not found",
    "details": "The symbol BTCUSDT is not supported"
  }
}
```

## 🔒 Rate Limiting

- **Market Data**: 100 requests/minute
- **Trading**: 10 requests/minute
- **DEX Operations**: 20 requests/minute

## 📱 Frontend Integration Examples

### JavaScript/TypeScript
```javascript
class TradingAPI {
  constructor(apiKey, baseURL = 'http://localhost:8000') {
    this.apiKey = apiKey;
    this.baseURL = baseURL;
  }

  async request(endpoint, options = {}) {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': this.apiKey,
        ...options.headers
      }
    });
    
    return response.json();
  }

  async getAccountInfo() {
    return this.request('/api/account/info');
  }

  async placeBuyOrder(symbol, quantity) {
    return this.request('/api/orders/buy/market', {
      method: 'POST',
      body: JSON.stringify({ symbol, quantity })
    });
  }

  async getDEXQuote(tokenIn, tokenOut, amount, chainId) {
    return this.request('/api/dex/quote', {
      method: 'POST',
      body: JSON.stringify({ tokenIn, tokenOut, amount, chainId })
    });
  }
}
```

### React Hook Example
```javascript
import { useState, useEffect } from 'react';

const useTradingAPI = (apiKey) => {
  const [accountInfo, setAccountInfo] = useState(null);
  const [loading, setLoading] = useState(false);

  const api = new TradingAPI(apiKey);

  const fetchAccountInfo = async () => {
    setLoading(true);
    try {
      const result = await api.getAccountInfo();
      setAccountInfo(result.data);
    } catch (error) {
      console.error('Failed to fetch account info:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAccountInfo();
  }, []);

  return { accountInfo, loading, refetch: fetchAccountInfo };
};
```
