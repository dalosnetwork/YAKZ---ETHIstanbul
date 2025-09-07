# Binance WebSocket Configuration

# WebSocket URLs
BINANCE_WS_BASE_URL = "wss://stream.binance.com:9443"
BINANCE_WS_ALTERNATIVE_URL = "wss://stream.binance.com:443"
BINANCE_DATA_STREAM_URL = "wss://data-stream.binance.vision"

# Stream endpoints
RAW_STREAM_ENDPOINT = "/ws/{stream_name}"
COMBINED_STREAM_ENDPOINT = "/stream?streams={streams}"

# Trading symbols to monitor
SYMBOLS = [
    'BTCUSDT',    # Bitcoin
    'ETHUSDT',    # Ethereum
    'BNBUSDT',    # Binance Coin
    'ADAUSDT',    # Cardano
    'SOLUSDT'     # Solana
]

# WebSocket settings
WS_PING_INTERVAL = 30  # seconds - Send pong every 30 seconds
WS_CONNECTION_TIMEOUT = 24 * 60 * 60  # 24 hours in seconds
WS_RECONNECT_DELAY = 5  # seconds to wait before reconnecting

# Stream types
STREAM_TYPES = {
    'DEPTH': 'depth',
    'TRADE': 'trade',
    'TICKER': 'ticker',
    'KLINE_1M': 'kline_1m',
    'KLINE_5M': 'kline_5m',
    'MINIticker': 'miniTicker',
    'BOOKTICKER': 'bookTicker'
}

# Default stream type for monitoring
DEFAULT_STREAM_TYPE = STREAM_TYPES['DEPTH']

# Display settings
MAX_DISPLAY_ORDERS = 5  # Number of bids/asks to display
TIMESTAMP_FORMAT = "%H:%M:%S"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
MICROSECOND_TIMESTAMP_FORMAT = "%H:%M:%S.%f"

# Time units
TIME_UNITS = {
    'MILLISECOND': 'millisecond',
    'MICROSECOND': 'microsecond'
}

DEFAULT_TIME_UNIT = TIME_UNITS['MILLISECOND']

# Additional popular symbols (for future expansion)
ADDITIONAL_SYMBOLS = [
    'DOGEUSDT',   # Dogecoin
    'XRPUSDT',    # Ripple
    'DOTUSDT',    # Polkadot
    'AVAXUSDT',   # Avalanche
    'MATICUSDT',  # Polygon
    'LINKUSDT',   # Chainlink
    'LTCUSDT',    # Litecoin
    'UNIUSDT',    # Uniswap
    'ATOMUSDT',   # Cosmos
    'FTMUSDT'     # Fantom
]

# Error messages
ERROR_MESSAGES = {
    'CONNECTION_FAILED': 'Failed to connect to Binance WebSocket',
    'JSON_DECODE_ERROR': 'Failed to decode JSON message',
    'PING_PONG_ERROR': 'Error in ping/pong handling',
    'MESSAGE_HANDLING_ERROR': 'Error handling WebSocket message',
    'UNEXPECTED_ERROR': 'An unexpected error occurred'
}

# Success messages
SUCCESS_MESSAGES = {
    'CONNECTED': 'Successfully connected to Binance WebSocket',
    'DISCONNECTED': 'WebSocket connection closed gracefully',
    'SHUTDOWN': 'Application shutting down...',
    'ORDER_PLACED': 'Order placed successfully',
    'ORDER_CANCELLED': 'Order cancelled successfully',
    'API_INITIALIZED': 'API client initialized successfully'
}

# Binance REST API Configuration
BINANCE_API_BASE_URL = {
    'MAINNET': 'https://api.binance.com',
    'TESTNET': 'https://testnet.binance.vision'
}

# API Endpoints
API_ENDPOINTS = {
    'EXCHANGE_INFO': '/api/v3/exchangeInfo',
    'ORDER': '/api/v3/order',
    'OPEN_ORDERS': '/api/v3/openOrders',
    'ALL_ORDERS': '/api/v3/allOrders',
    'ACCOUNT': '/api/v3/account',
    'TICKER_PRICE': '/api/v3/ticker/price',
    'TICKER_24HR': '/api/v3/ticker/24hr',
    'DEPTH': '/api/v3/depth',
    'TRADES': '/api/v3/trades',
    'KLINES': '/api/v3/klines'
}

# Order Types
ORDER_TYPES = {
    'LIMIT': 'LIMIT',
    'MARKET': 'MARKET',
    'STOP_LOSS': 'STOP_LOSS',
    'STOP_LOSS_LIMIT': 'STOP_LOSS_LIMIT',
    'TAKE_PROFIT': 'TAKE_PROFIT',
    'TAKE_PROFIT_LIMIT': 'TAKE_PROFIT_LIMIT',
    'LIMIT_MAKER': 'LIMIT_MAKER'
}

# Order Sides
ORDER_SIDES = {
    'BUY': 'BUY',
    'SELL': 'SELL'
}

# Time in Force
TIME_IN_FORCE = {
    'GTC': 'GTC',  # Good Till Cancelled
    'IOC': 'IOC',  # Immediate or Cancel
    'FOK': 'FOK'   # Fill or Kill
}

# Order Status
ORDER_STATUS = {
    'NEW': 'NEW',
    'PARTIALLY_FILLED': 'PARTIALLY_FILLED',
    'FILLED': 'FILLED',
    'CANCELED': 'CANCELED',
    'PENDING_CANCEL': 'PENDING_CANCEL',
    'REJECTED': 'REJECTED',
    'EXPIRED': 'EXPIRED'
}

# API Rate Limits (requests per minute)
API_RATE_LIMITS = {
    'ORDER': 10,          # 10 orders per second
    'REQUEST': 1200,      # 1200 requests per minute
    'RAW_REQUEST': 6000   # 6000 requests per 5 minutes
}

# Order Size Limits (example values - should be fetched from exchange info)
DEFAULT_ORDER_LIMITS = {
    'MIN_NOTIONAL': 10.0,  # Minimum order value in USDT
    'MAX_POSITION': 1000000.0,  # Maximum position size
    'MIN_QTY': 0.00001,    # Minimum quantity
    'MAX_QTY': 9000000.0   # Maximum quantity
}

# Risk Management Settings
RISK_MANAGEMENT = {
    'MAX_ORDER_SIZE_PERCENT': 10.0,  # Max 10% of balance per order
    'MAX_DAILY_ORDERS': 100,         # Maximum orders per day
    'SLIPPAGE_TOLERANCE': 0.005,     # 0.5% slippage tolerance
    'MIN_SPREAD': 0.001              # Minimum spread for limit orders
}

# Authentication Settings
API_SETTINGS = {
    'RECV_WINDOW': 60000,      # 60 seconds receive window
    'TIMEOUT': 30,             # 30 seconds request timeout
    'RETRY_ATTEMPTS': 3,       # Number of retry attempts
    'RETRY_DELAY': 1           # Delay between retries in seconds
} 
# Smart Contract Configuration
SMART_CONTRACT_RPC_URL = "https://mainnet.infura.io/v3/YOUR_PROJECT_ID"
SMART_CONTRACT_ADDRESS = "0x..."  # Your contract address
SMART_CONTRACT_ABI = [
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "name": "exType", "type": "string"},
            {"indexed": False, "name": "quantity", "type": "uint256"},
            {"indexed": False, "name": "expectedPrice", "type": "uint256"},
            {"indexed": False, "name": "pair", "type": "string"},
            {"indexed": False, "name": "side", "type": "string"}
        ],
        "name": "TradingSignal",
        "type": "event"
    }
]

# Odos Configuration  
ODOS_API_KEY = "your_odos_api_key"
ODOS_CHAIN_ID = 8453  # Base mainnet
ODOS_BASE_URL = "https://api.odos.xyz"

# Risk Management
MAX_TRADE_SIZE = 10000  # USDT
MAX_POSITION_RATIO = 0.1  # 10% of portfolio
MIN_TRADE_SIZE = 0.001  # Minimum trade amount

# Token Addresses (Ethereum Mainnet)
TOKEN_ADDRESSES = {
    "ETH": "0x0000000000000000000000000000000000000000",  # WETH
    "BTC": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",  # WBTC
    "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",  # USDT
    "USDC": "0xA0b86a33E6441b8c4C8C0e4b8b8b8b8b8b8b8b8b",  # USDC
    "SOL": "0xD31a59c85aE9D8edEFeC411D448f90841571b89c",  # SOL
    "ADA": "0x3EE2200Efb3400fAbB9AacF31297cBdD1d435D47",  # ADA
}

# Wallet Configuration
WALLET_ADDRESS = "0x0000000000000000000000000000000000000000"  # Your wallet address
PRIVATE_KEY = "your_private_key"  # Keep this secure!

# ===========================================
# ENVIRONMENT VARIABLES
# ===========================================
import os

# Load from .env file
def get_env(key: str, default: str = None) -> str:
    """Get environment variable with default value."""
    return os.getenv(key, default)

# Override with environment variables
SMART_CONTRACT_RPC_URL = get_env('SMART_CONTRACT_RPC_URL', SMART_CONTRACT_RPC_URL)
SMART_CONTRACT_ADDRESS = get_env('SMART_CONTRACT_ADDRESS', SMART_CONTRACT_ADDRESS)
ODOS_API_KEY = get_env('ODOS_API_KEY', ODOS_API_KEY)
WALLET_ADDRESS = get_env('WALLET_ADDRESS', WALLET_ADDRESS)
PRIVATE_KEY = get_env('PRIVATE_KEY', PRIVATE_KEY)
MAX_TRADE_SIZE = int(get_env('MAX_TRADE_SIZE', str(MAX_TRADE_SIZE)))
MAX_POSITION_RATIO = float(get_env('MAX_POSITION_RATIO', str(MAX_POSITION_RATIO)))
MIN_TRADE_SIZE = float(get_env('MIN_TRADE_SIZE', str(MIN_TRADE_SIZE)))
DEBUG_MODE = get_env('DEBUG_MODE', 'False').lower() == 'true'
