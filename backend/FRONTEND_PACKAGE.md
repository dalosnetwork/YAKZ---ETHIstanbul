# 🚀 Frontend Integration Package

Bu paket, trading sisteminizi frontend uygulamanızla entegre etmek için gerekli tüm dosyaları içerir.

## 📦 Paket İçeriği

### 📁 `frontend_integration/`
- **`trading-sdk.js`** - JavaScript SDK (Vanilla JS için)
- **`useTradingAPI.js`** - React Hooks (React uygulamaları için)
- **`trading-api.d.ts`** - TypeScript definitions
- **`INTEGRATION_GUIDE.md`** - Detaylı entegrasyon rehberi
- **`example.html`** - Çalışan örnek HTML sayfası

### 📁 `api_docs/`
- **`API_ENDPOINTS.md`** - Tüm API endpoint'lerinin dokümantasyonu

### 📁 Root Files
- **`api_server.py`** - FastAPI server (Python backend)
- **`FRONTEND_PACKAGE.md`** - Bu dosya

## 🚀 Hızlı Başlangıç

### 1. Backend'i Başlatın
```bash
# Python dependencies
pip install fastapi uvicorn

# Environment variables (.env dosyasında)
FRONTEND_API_KEY=your_frontend_api_key_here
BINANCE_API_KEY=your_binance_api_key
BINANCE_API_SECRET=your_binance_api_secret
ODOS_API_KEY=your_odos_api_key

# Server'ı başlatın
python api_server.py
```

### 2. Frontend'i Test Edin
```bash
# Örnek HTML sayfasını açın
open frontend_integration/example.html
# veya
python -m http.server 8001
# Sonra http://localhost:8001/frontend_integration/example.html
```

### 3. API'yi Test Edin
```bash
# Health check
curl http://localhost:8000/api/health

# API docs
open http://localhost:8000/docs
```

## 📱 Frontend Entegrasyonu

### Vanilla JavaScript
```html
<script src="trading-sdk.js"></script>
<script>
const api = new TradingAPI('your_api_key', 'http://localhost:8000');
const accountInfo = await api.getAccountInfo();
</script>
```

### React
```jsx
import { useAccountInfo, useTrading } from './useTradingAPI.js';

function TradingApp({ apiKey }) {
  const { accountInfo } = useAccountInfo(apiKey);
  const { placeBuyOrder } = useTrading(apiKey);
  
  return <div>{/* Your component */}</div>;
}
```

### TypeScript
```typescript
import { TradingAPI, AccountInfo } from './trading-api.d.ts';

const api = new TradingAPI('your_api_key');
const accountInfo: AccountInfo = await api.getAccountInfo();
```

## 🔧 API Endpoints

### Temel Endpoints
- `GET /api/health` - Health check
- `GET /api/status` - System status
- `GET /api/account/info` - Account information
- `GET /api/account/balance/{asset}` - Asset balance

### Trading Endpoints
- `POST /api/orders/buy/market` - Market buy order
- `POST /api/orders/sell/market` - Market sell order
- `DELETE /api/orders/{orderId}` - Cancel order

### DEX Endpoints
- `POST /api/dex/quote` - Get DEX quote
- `POST /api/dex/assemble` - Assemble DEX transaction

### WebSocket
- `ws://localhost:8000/ws` - Real-time updates

## 🔑 Authentication

Tüm API çağrıları için `X-API-Key` header'ı gerekli:

```javascript
const api = new TradingAPI('your_api_key');
// SDK otomatik olarak header'ı ekler
```

## �� Desteklenen Özellikler

### ✅ CEX Trading
- Binance spot trading
- Market buy/sell orders
- Order cancellation
- Account balance checking

### ✅ DEX Trading
- ODOS API integration
- Multi-chain support (Base, Ethereum, Polygon, Arbitrum, Optimism)
- Quote generation
- Transaction assembly

### ✅ Real-time Updates
- WebSocket connection
- System status monitoring
- Event broadcasting

### ✅ Risk Management
- Position sizing
- Balance validation
- Trade size limits

## 🌐 Desteklenen Chain'ler

- **Base** (Chain ID: 8453) - WETH, USDC, USDT
- **Ethereum** (Chain ID: 1) - WETH, USDC, USDT, DAI
- **Polygon** (Chain ID: 137) - WMATIC, USDC, USDT, DAI
- **Arbitrum** (Chain ID: 42161) - WETH, USDC, USDT, ARB
- **Optimism** (Chain ID: 10) - WETH, USDC, USDT, OP

## 🔒 Güvenlik

- API key authentication
- CORS protection
- Rate limiting
- Input validation
- Error handling

## 📞 Destek

- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health
- **Example App**: `frontend_integration/example.html`

## 🚀 Production Deployment

1. **Environment Variables**: Production API keys'leri ayarlayın
2. **CORS**: Frontend domain'inizi CORS ayarlarına ekleyin
3. **HTTPS**: SSL certificate kullanın
4. **Rate Limiting**: Production rate limit'lerini ayarlayın

---

**Hazır!** 🎉 Frontend'inizi trading sisteminizle entegre etmek için her şey hazır!
