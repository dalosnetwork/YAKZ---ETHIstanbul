# 🚀 Frontend Integration Guide

Bu rehber, trading sisteminizi frontend uygulamanızla entegre etmek için gerekli tüm bilgileri içerir.

## 📋 İçindekiler

1. [Kurulum](#kurulum)
2. [API Server Başlatma](#api-server-başlatma)
3. [JavaScript SDK Kullanımı](#javascript-sdk-kullanımı)
4. [React Entegrasyonu](#react-entegrasyonu)
5. [WebSocket Bağlantısı](#websocket-bağlantısı)
6. [Örnek Uygulamalar](#örnek-uygulamalar)
7. [Hata Yönetimi](#hata-yönetimi)
8. [Güvenlik](#güvenlik)

## 🛠️ Kurulum

### 1. Gerekli Dosyaları Kopyalayın

Frontend projenize şu dosyaları kopyalayın:

```
frontend_integration/
├── trading-sdk.js          # JavaScript SDK
├── useTradingAPI.js        # React Hooks
├── trading-api.d.ts        # TypeScript Definitions
└── INTEGRATION_GUIDE.md    # Bu rehber
```

### 2. NPM Paketleri (Opsiyonel)

```bash
npm install axios  # HTTP istekleri için
npm install @types/node  # TypeScript için
```

## 🚀 API Server Başlatma

### 1. Python Dependencies

```bash
pip install fastapi uvicorn websockets
```

### 2. Environment Variables

`.env` dosyanızda şu değişkenleri ayarlayın:

```env
# Frontend API Key
FRONTEND_API_KEY=your_frontend_api_key_here

# Binance API (mevcut)
BINANCE_API_KEY=your_binance_api_key
BINANCE_API_SECRET=your_binance_api_secret

# ODOS API (mevcut)
ODOS_API_KEY=your_odos_api_key

# Diğer ayarlar...
```

### 3. Server'ı Başlatın

```bash
python api_server.py
```

Server şu adreslerde çalışacak:
- **API**: http://localhost:8000
- **WebSocket**: ws://localhost:8000/ws
- **API Docs**: http://localhost:8000/docs

## 📱 JavaScript SDK Kullanımı

### Temel Kullanım

```javascript
// SDK'yı import edin
import TradingAPI from './trading-sdk.js';

// API instance oluşturun
const api = new TradingAPI('your_api_key', 'http://localhost:8000');

// Hesap bilgilerini alın
const accountInfo = await api.getAccountInfo();
console.log('Account:', accountInfo.data);

// Bakiye sorgulayın
const balance = await api.getBalance('USDT');
console.log('USDT Balance:', balance.data.balance);

// Market buy order verin
const order = await api.placeBuyOrder('BTCUSDT', 0.001);
console.log('Order placed:', order.data);
```

### DEX İşlemleri

```javascript
// DEX quote alın
const quote = await api.getDEXQuote(
  '0x833589fcd6edb6e08f4c7c32d4f71b54bda02913', // USDC
  '0x4200000000000000000000000000000000000006', // WETH
  '1000000000000000', // 0.001 USDC (wei)
  8453 // Base chain
);

console.log('DEX Quote:', quote.data);

// Transaction assemble edin
const txData = await api.assembleDEXTransaction(
  quote.data.pathId,
  '0x742d35Cc6634C0532925a3b8D0C0C4C2C2C2C2C2'
);

console.log('Transaction:', txData.data);
```

### Event Triggering

```javascript
// Trading event tetikleyin
const eventData = api.formatTradingEvent('cex', 0.001, 50000, 'BTC', 'buy');
await api.triggerEvent(eventData);

// Veya doğrudan parametrelerle
await api.triggerEvent('|dex|0.001|2000|ETH|buy|');
```

## ⚛️ React Entegrasyonu

### 1. Hooks'ları Import Edin

```javascript
import { 
  useAccountInfo, 
  useBalance, 
  useTrading, 
  useDEX,
  useWebSocket 
} from './useTradingAPI.js';
```

### 2. Temel React Component

```jsx
import React from 'react';
import { useAccountInfo, useTrading } from './useTradingAPI.js';

function TradingDashboard({ apiKey }) {
  const { accountInfo, loading: accountLoading } = useAccountInfo(apiKey);
  const { placeBuyOrder, placeSellOrder, loading: tradingLoading } = useTrading(apiKey);

  const handleBuy = async () => {
    try {
      const order = await placeBuyOrder('BTCUSDT', 0.001);
      console.log('Buy order placed:', order);
    } catch (error) {
      console.error('Buy order failed:', error);
    }
  };

  const handleSell = async () => {
    try {
      const order = await placeSellOrder('BTCUSDT', 0.001);
      console.log('Sell order placed:', order);
    } catch (error) {
      console.error('Sell order failed:', error);
    }
  };

  if (accountLoading) return <div>Loading account info...</div>;

  return (
    <div>
      <h2>Trading Dashboard</h2>
      {accountInfo && (
        <div>
          <p>Account Type: {accountInfo.accountType}</p>
          <p>Can Trade: {accountInfo.canTrade ? 'Yes' : 'No'}</p>
          <div>
            <h3>Balances:</h3>
            {accountInfo.balances.map(balance => (
              <p key={balance.asset}>
                {balance.asset}: {balance.free}
              </p>
            ))}
          </div>
        </div>
      )}
      
      <div>
        <button onClick={handleBuy} disabled={tradingLoading}>
          Buy BTC
        </button>
        <button onClick={handleSell} disabled={tradingLoading}>
          Sell BTC
        </button>
      </div>
    </div>
  );
}

export default TradingDashboard;
```

### 3. DEX Trading Component

```jsx
import React, { useState } from 'react';
import { useDEX } from './useTradingAPI.js';

function DEXTrading({ apiKey }) {
  const { getQuote, assembleTransaction, loading } = useDEX(apiKey);
  const [quote, setQuote] = useState(null);
  const [txData, setTxData] = useState(null);

  const handleGetQuote = async () => {
    try {
      const result = await getQuote(
        '0x833589fcd6edb6e08f4c7c32d4f71b54bda02913', // USDC
        '0x4200000000000000000000000000000000000006', // WETH
        '1000000000000000', // 0.001 USDC
        8453 // Base chain
      );
      setQuote(result);
    } catch (error) {
      console.error('Quote failed:', error);
    }
  };

  const handleAssemble = async () => {
    if (!quote) return;
    
    try {
      const result = await assembleTransaction(
        quote.pathId,
        '0x742d35Cc6634C0532925a3b8D0C0C4C2C2C2C2C2'
      );
      setTxData(result);
    } catch (error) {
      console.error('Assemble failed:', error);
    }
  };

  return (
    <div>
      <h3>DEX Trading</h3>
      
      <button onClick={handleGetQuote} disabled={loading}>
        Get Quote
      </button>
      
      {quote && (
        <div>
          <p>Input: {quote.inValues[0]} USDC</p>
          <p>Output: {quote.outValues[0]} WETH</p>
          <p>Gas: {quote.gasEstimate}</p>
          <p>Price Impact: {quote.priceImpact}%</p>
          
          <button onClick={handleAssemble} disabled={loading}>
            Assemble Transaction
          </button>
        </div>
      )}
      
      {txData && (
        <div>
          <h4>Transaction Ready:</h4>
          <p>To: {txData.transaction.to}</p>
          <p>Gas: {txData.transaction.gas}</p>
          <p>Data: {txData.transaction.data.substring(0, 50)}...</p>
        </div>
      )}
    </div>
  );
}

export default DEXTrading;
```

## 🔌 WebSocket Bağlantısı

### Real-time Updates

```jsx
import React, { useEffect, useState } from 'react';
import { useWebSocket } from './useTradingAPI.js';

function RealTimeUpdates({ apiKey }) {
  const { connected, messages, connect, disconnect } = useWebSocket(apiKey);
  const [lastMessage, setLastMessage] = useState(null);

  useEffect(() => {
    connect();
    return () => disconnect();
  }, [connect, disconnect]);

  useEffect(() => {
    if (messages.length > 0) {
      setLastMessage(messages[messages.length - 1]);
    }
  }, [messages]);

  return (
    <div>
      <h3>Real-time Updates</h3>
      <p>Status: {connected ? 'Connected' : 'Disconnected'}</p>
      
      {lastMessage && (
        <div>
          <h4>Last Update:</h4>
          <pre>{JSON.stringify(lastMessage, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default RealTimeUpdates;
```

## 📱 Örnek Uygulamalar

### 1. Basit Trading App

```jsx
import React, { useState } from 'react';
import { useAccountInfo, useTrading, useBalance } from './useTradingAPI.js';

function SimpleTradingApp() {
  const [apiKey, setApiKey] = useState('');
  const [symbol, setSymbol] = useState('BTCUSDT');
  const [quantity, setQuantity] = useState(0.001);
  
  const { accountInfo } = useAccountInfo(apiKey);
  const { placeBuyOrder, placeSellOrder, loading } = useTrading(apiKey);
  const { balance: usdtBalance } = useBalance(apiKey, 'USDT');

  return (
    <div style={{ padding: '20px' }}>
      <h1>Simple Trading App</h1>
      
      <div style={{ marginBottom: '20px' }}>
        <input
          type="text"
          placeholder="API Key"
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
        />
      </div>

      {accountInfo && (
        <div style={{ marginBottom: '20px' }}>
          <h3>Account Info</h3>
          <p>Type: {accountInfo.accountType}</p>
          <p>USDT Balance: {usdtBalance}</p>
        </div>
      )}

      <div style={{ marginBottom: '20px' }}>
        <input
          type="text"
          placeholder="Symbol"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
        />
        <input
          type="number"
          placeholder="Quantity"
          value={quantity}
          onChange={(e) => setQuantity(parseFloat(e.target.value))}
          step="0.001"
        />
      </div>

      <div>
        <button
          onClick={() => placeBuyOrder(symbol, quantity)}
          disabled={loading}
          style={{ marginRight: '10px' }}
        >
          Buy
        </button>
        <button
          onClick={() => placeSellOrder(symbol, quantity)}
          disabled={loading}
        >
          Sell
        </button>
      </div>
    </div>
  );
}

export default SimpleTradingApp;
```

### 2. DEX Swapping Interface

```jsx
import React, { useState } from 'react';
import { useDEX } from './useTradingAPI.js';

function DEXSwappingInterface({ apiKey }) {
  const { getQuote, assembleTransaction, loading } = useDEX(apiKey);
  const [fromToken, setFromToken] = useState('USDC');
  const [toToken, setToToken] = useState('WETH');
  const [amount, setAmount] = useState('0.001');
  const [quote, setQuote] = useState(null);
  const [txData, setTxData] = useState(null);

  const tokenAddresses = {
    USDC: '0x833589fcd6edb6e08f4c7c32d4f71b54bda02913',
    WETH: '0x4200000000000000000000000000000000000006',
    USDT: '0x833589fcd6edb6e08f4c7c32d4f71b54bda02913'
  };

  const handleSwap = async () => {
    try {
      // 1. Get quote
      const amountWei = (parseFloat(amount) * 1e18).toString();
      const quoteResult = await getQuote(
        tokenAddresses[fromToken],
        tokenAddresses[toToken],
        amountWei,
        8453 // Base chain
      );
      setQuote(quoteResult);

      // 2. Assemble transaction
      const txResult = await assembleTransaction(
        quoteResult.pathId,
        '0x742d35Cc6634C0532925a3b8D0C0C4C2C2C2C2C2'
      );
      setTxData(txResult);

    } catch (error) {
      console.error('Swap failed:', error);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>DEX Swapping</h2>
      
      <div style={{ marginBottom: '20px' }}>
        <select value={fromToken} onChange={(e) => setFromToken(e.target.value)}>
          <option value="USDC">USDC</option>
          <option value="USDT">USDT</option>
        </select>
        
        <input
          type="number"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          step="0.001"
        />
        
        <select value={toToken} onChange={(e) => setToToken(e.target.value)}>
          <option value="WETH">WETH</option>
          <option value="USDC">USDC</option>
        </select>
      </div>

      <button onClick={handleSwap} disabled={loading}>
        {loading ? 'Processing...' : 'Get Quote & Swap'}
      </button>

      {quote && (
        <div style={{ marginTop: '20px' }}>
          <h3>Quote</h3>
          <p>Input: {quote.inValues[0]} {fromToken}</p>
          <p>Output: {quote.outValues[0]} {toToken}</p>
          <p>Gas: {quote.gasEstimate}</p>
          <p>Price Impact: {quote.priceImpact}%</p>
        </div>
      )}

      {txData && (
        <div style={{ marginTop: '20px' }}>
          <h3>Transaction Ready</h3>
          <p>To: {txData.transaction.to}</p>
          <p>Gas: {txData.transaction.gas}</p>
          <p>Value: {txData.transaction.value} ETH</p>
        </div>
      )}
    </div>
  );
}

export default DEXSwappingInterface;
```

## ⚠️ Hata Yönetimi

### Error Handling Best Practices

```javascript
// API çağrılarında hata yakalama
try {
  const result = await api.placeBuyOrder('BTCUSDT', 0.001);
  console.log('Success:', result.data);
} catch (error) {
  if (error.message.includes('401')) {
    console.error('Authentication failed - check API key');
  } else if (error.message.includes('400')) {
    console.error('Invalid request - check parameters');
  } else if (error.message.includes('500')) {
    console.error('Server error - try again later');
  } else {
    console.error('Unknown error:', error.message);
  }
}

// React hook'larda error handling
function TradingComponent({ apiKey }) {
  const { accountInfo, error, refetch } = useAccountInfo(apiKey);

  if (error) {
    return (
      <div>
        <p>Error: {error}</p>
        <button onClick={refetch}>Retry</button>
      </div>
    );
  }

  return <div>{/* Your component */}</div>;
}
```

## 🔒 Güvenlik

### 1. API Key Güvenliği

```javascript
// API key'i environment variable'dan alın
const apiKey = process.env.REACT_APP_TRADING_API_KEY;

// Veya kullanıcıdan güvenli şekilde alın
const [apiKey, setApiKey] = useState('');

// API key'i localStorage'da saklamayın (güvenlik riski)
// Bunun yerine session storage veya secure cookie kullanın
```

### 2. HTTPS Kullanın

Production'da mutlaka HTTPS kullanın:

```javascript
const api = new TradingAPI(apiKey, 'https://your-domain.com');
```

### 3. Rate Limiting

API'nin rate limit'lerini göz önünde bulundurun:

```javascript
// Çok sık API çağrısı yapmayın
const debouncedFetch = useCallback(
  debounce(() => {
    fetchAccountInfo();
  }, 1000),
  []
);
```

## 📞 Destek

Herhangi bir sorunuz varsa:

1. **API Docs**: http://localhost:8000/docs
2. **Health Check**: http://localhost:8000/api/health
3. **System Status**: http://localhost:8000/api/status

## 🚀 Production Deployment

### 1. Environment Variables

```env
# Production .env
FRONTEND_API_KEY=your_secure_api_key
BINANCE_API_KEY=your_binance_key
BINANCE_API_SECRET=your_binance_secret
ODOS_API_KEY=your_odos_key
```

### 2. CORS Configuration

```python
# api_server.py'de CORS ayarlarını güncelleyin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)
```

### 3. SSL Certificate

HTTPS için SSL certificate kullanın:

```bash
# Nginx ile reverse proxy
server {
    listen 443 ssl;
    server_name your-api-domain.com;
    
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Bu rehber ile frontend'inizi trading sisteminizle kolayca entegre edebilirsiniz! 🎉
