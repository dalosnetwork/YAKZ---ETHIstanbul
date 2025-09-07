# 🚀 Binance Trading Bot with Contract Integration

A complete cryptocurrency trading system that combines real-time market data monitoring with automated trading execution based on smart contract events.

## 📋 Project Overview

This project provides a **modular trading system** with three main components:

1. **📊 Real-time Market Data** - WebSocket monitoring of cryptocurrency prices
2. **🏦 Spot Trading** - Automated buy/sell orders on Binance
3. **🔗 Contract Integration** - Event-driven trading based on smart contract signals

## 🏗️ Project Structure

```
roar/
├── main.py                    # 🚀 Main application entry point
├── requirements.txt           # 📦 Python dependencies
├── env.example               # 🔐 Environment configuration template
├── README.md                 # 📚 This documentation
│
├── config/                   # ⚙️ Configuration files
│   ├── settings.py           #   Application settings & API endpoints
│   └── __init__.py
│
├── src/                      # 💻 Source code modules
│   ├── websocket_client.py   #   📡 Real-time market data via WebSocket
│   ├── order_client.py       #   🏦 Binance trading API client
│   ├── order_types.py        #   📋 Order classes & validation
│   ├── business_service.py   #   🧠 Contract event processing & trading
│   ├── config_loader.py      #   🔧 Environment variable management
│   ├── utils.py              #   🛠️ Helper functions
│   └── __init__.py
│
└── examples/                 # 📚 Usage examples
    ├── order_examples.py     #   🏦 Trading examples
    └── cex_transaction_example.py  # 🔗 Contract event examples
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the project
git clone <your-repo-url>
cd roar

# Install dependencies
pip3 install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
cp env.example .env

# Edit .env with your API credentials
nano .env
```

**Required Configuration:**
```bash
# Binance API (required for trading)
BINANCE_API_KEY=your_binance_api_key
BINANCE_API_SECRET=your_binance_api_secret

# Optional settings
USE_TESTNET=True                    # Safe testing environment
ENABLE_BUSINESS_SERVICE=True        # Enable automated trading
TRADING_SYMBOLS=BTCUSDT,ETHUSDT     # Symbols to monitor
```

### 3. Run the Application

```bash
# Start the complete system
python3 main.py
```

## 🔧 Core Components

### 📡 WebSocket Market Data (`websocket_client.py`)

**What it does:**
- Connects to Binance WebSocket API
- Monitors real-time price depth for 5 cryptocurrencies
- Displays live order book data in terminal

**Features:**
- ✅ Real-time market depth monitoring
- ✅ Automatic ping/pong handling
- ✅ Graceful error handling
- ✅ Configurable symbols

**Usage:**
```python
from src.websocket_client import BinanceWebSocket

# Monitor market depth
ws = BinanceWebSocket(['BTCUSDT', 'ETHUSDT'], 'depth')
await ws.connect()
```

### 🏦 Trading System (`order_client.py` + `order_types.py`)

**What it does:**
- Executes buy/sell orders on Binance
- Handles market and limit orders
- Manages order validation and risk

**Features:**
- ✅ Market orders (instant execution)
- ✅ Limit orders (price-specific execution)
- ✅ Order management (cancel, status, history)
- ✅ Account balance checking
- ✅ Parameter validation

**Usage:**
```python
from src.order_client import BinanceOrderClient

# Initialize trading client
client = BinanceOrderClient(api_key, api_secret, testnet=True)

# Place orders
client.place_market_buy_order('BTCUSDT', quote_order_qty=100.0)
client.place_limit_sell_order('ETHUSDT', quantity=0.1, price=2500.0)
```

### 🧠 Business Logic (`business_service.py`)

**What it does:**
- Processes smart contract events
- Executes automated trading decisions
- Routes between CEX (Binance) and DEX (Odos) trading

**Event Format:**
```
|ex_type|quantity|expected_price|pair|transaction_side|
|cex|4200|0.5|ETH|buy|
```

**Features:**
- ✅ Contract event parsing
- ✅ CEX/DEX routing
- ✅ Business rule processing
- ✅ Risk management integration points

**Usage:**
```python
from src.business_service import BusinessService

# Initialize business service
service = BusinessService(api_key, api_secret, testnet=True)

# Handle contract events
await service.handle_cex_transaction_event("|cex|4200|0.5|ETH|buy|")
```

## 🎯 Trading Modes

### 1. 📊 Market Data Only
```bash
# Run without API keys (WebSocket only)
python3 main.py
```
- Monitors real-time prices
- No trading functionality
- Safe for testing

### 2. 🏦 Full Trading System
```bash
# Run with API keys in .env
python3 main.py
```
- Market data monitoring
- Automated trading
- Contract event processing

## 🔗 Contract Integration

### Event Structure
The system expects contract events in this format:
```
|exchange_type|quantity|expected_price|pair|side|
```

**Examples:**
- `|cex|4200|0.5|ETH|buy|` - Buy 0.5 ETH for $4200 on CEX
- `|dex|2500|1.0|BTC|sell|` - Sell 1.0 BTC for $2500 on DEX

### Integration Points

**For Contract Developers:**
1. **Event Listener** - Implement in `business_service.py` `start()` method
2. **Event Processing** - Call `handle_cex_transaction_event(event_data)`

**For Business Logic:**
- Look for `**PUT OPERATIONS BUSINESS HERE**` comments
- Add risk management, position sizing, etc.

**For DEX Integration:**
- Look for `**PUT ODOS OPERATIONS HERE**` comments
- Implement Odos API integration

## 📚 Examples

### Basic Trading Example
```python
# examples/order_examples.py
from src.order_client import BinanceOrderClient

client = BinanceOrderClient(api_key, api_secret, testnet=True)

# Market buy
client.place_market_buy_order('BTCUSDT', quote_order_qty=50.0)

# Limit sell
client.place_limit_sell_order('ETHUSDT', quantity=0.1, price=2500.0)
```

### Contract Event Example
```python
# examples/cex_transaction_example.py
from src.business_service import BusinessService

service = BusinessService(api_key, api_secret, testnet=True)

# Handle contract events
await service.handle_cex_transaction_event("|cex|4200|0.5|ETH|buy|")
await service.handle_cex_transaction_event("|dex|2500|1.0|BTC|sell|")
```

## ⚙️ Configuration

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `BINANCE_API_KEY` | Binance API key | Required |
| `BINANCE_API_SECRET` | Binance API secret | Required |
| `USE_TESTNET` | Use testnet for safety | `True` |
| `ENABLE_BUSINESS_SERVICE` | Enable trading | `True` |
| `TRADING_SYMBOLS` | Symbols to monitor | `BTCUSDT,ETHUSDT,BNBUSDT,ADAUSDT,SOLUSDT` |

### Application Settings
- **WebSocket URLs** - Binance streaming endpoints
- **API Endpoints** - Trading and account endpoints
- **Order Types** - Market, limit, stop-loss orders
- **Risk Management** - Position limits, daily limits

## 🛡️ Safety Features

### Testnet Support
- ✅ Default to testnet for safe testing
- ✅ No real money at risk during development
- ✅ Full functionality testing

### Risk Management
- ✅ API key validation
- ✅ Order size limits
- ✅ Error handling and recovery
- ✅ Graceful shutdown

### Security
- ✅ Environment variable configuration
- ✅ No hardcoded credentials
- ✅ Secure API communication

## 🔧 Development

### Adding New Features

**New Order Types:**
1. Add to `src/order_types.py`
2. Implement in `src/order_client.py`
3. Update business service

**New Event Types:**
1. Add to `business_service.py` enums
2. Implement parsing logic
3. Add execution handlers

**New Exchanges:**
1. Create new client in `src/`
2. Add to business service routing
3. Implement integration points

### Integration Points

**Contract Event Listeners:**
```python
# In business_service.py start() method
# **PUT OPERATIONS BUSINESS HERE**
# - Implement your contract event listeners
# - Call handle_cex_transaction_event() when events arrive
```

**Business Logic:**
```python
# Look for these comments throughout the code:
# **PUT OPERATIONS BUSINESS HERE**
# - Risk management
# - Position sizing
# - Market analysis
```

**DEX Integration:**
```python
# Look for these comments in DEX functions:
# **PUT ODOS OPERATIONS HERE**
# - Odos API calls
# - Swap execution
# - Transaction monitoring
```

## 📊 Monitoring

### Real-time Output
- Live market depth updates
- Order execution confirmations
- Contract event processing
- Error messages and warnings

### Performance Tracking
- Order success/failure rates
- Event processing statistics
- System health monitoring

## 🚨 Troubleshooting

### Common Issues

**API Errors:**
- Check API key configuration
- Verify testnet vs mainnet settings
- Ensure sufficient account balance

**WebSocket Issues:**
- Check internet connection
- Verify Binance service status
- Review firewall settings

**Event Processing:**
- Validate event data format
- Check business service configuration
- Review error logs

### Getting Help

1. Check the examples in `examples/` directory
2. Review configuration in `config/settings.py`
3. Test with testnet first
4. Enable debug logging

## 📄 License

This project is for educational purposes. Please refer to Binance's API documentation for official usage guidelines.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Test thoroughly
5. Submit a pull request

---

**⚠️ Important:** Always test with testnet before using real funds. Trading cryptocurrencies involves risk.
