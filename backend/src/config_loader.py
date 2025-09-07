import os
from typing import Optional, List

class ConfigLoader:
    """
    Configuration loader that reads environment variables.
    Supports .env file loading and provides safe defaults.
    """
    
    def __init__(self, env_file: str = '.env'):
        """
        Initialize the config loader.
        
        Args:
            env_file (str): Path to environment file
        """
        self.env_file = env_file
        self._load_env_file()
    
    def _load_env_file(self) -> None:
        """Load environment variables from .env file if it exists."""
        if os.path.exists(self.env_file):
            try:
                with open(self.env_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        # Skip empty lines and comments
                        if not line or line.startswith('#'):
                            continue
                        
                        # Parse key=value pairs
                        if '=' in line:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip()
                            
                            # Remove quotes if present
                            if value.startswith('"') and value.endswith('"'):
                                value = value[1:-1]
                            elif value.startswith("'") and value.endswith("'"):
                                value = value[1:-1]
                            
                            # Set environment variable if not already set
                            if key not in os.environ:
                                os.environ[key] = value
                                
                print(f"✅ Loaded configuration from {self.env_file}")
            except Exception as e:
                print(f"⚠️  Warning: Could not load {self.env_file}: {e}")
        else:
            print(f"ℹ️  No {self.env_file} file found, using environment variables")
    
    def get_api_key(self) -> Optional[str]:
        """Get Binance API key from environment."""
        return os.getenv('BINANCE_API_KEY')
    
    def get_api_secret(self) -> Optional[str]:
        """Get Binance API secret from environment."""
        return os.getenv('BINANCE_API_SECRET')
    
    def use_testnet(self) -> bool:
        """Check if testnet should be used."""
        return os.getenv('USE_TESTNET', 'True').lower() in ('true', '1', 'yes', 'on')
    
    def enable_business_service(self) -> bool:
        """Check if business service should be enabled."""
        return os.getenv('ENABLE_BUSINESS_SERVICE', 'True').lower() in ('true', '1', 'yes', 'on')
    
    def get_trading_symbols(self) -> List[str]:
        """Get trading symbols from environment or use defaults."""
        symbols_env = os.getenv('TRADING_SYMBOLS')
        if symbols_env:
            return [s.strip().upper() for s in symbols_env.split(',')]
        
        # Default symbols
        return ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT', 'SOLUSDT']
    
    def get_max_order_amount(self) -> float:
        """Get maximum order amount from environment."""
        try:
            return float(os.getenv('MAX_ORDER_AMOUNT', '100.0'))
        except ValueError:
            return 100.0
    
    def get_log_level(self) -> str:
        """Get log level from environment."""
        return os.getenv('LOG_LEVEL', 'INFO').upper()
    
    def validate_config(self) -> bool:
        """
        Validate that required configuration is present.
        
        Returns:
            bool: True if config is valid
        """
        api_key = self.get_api_key()
        api_secret = self.get_api_secret()
        
        if not api_key or api_key == 'your_binance_api_key_here':
            print("❌ BINANCE_API_KEY not set or using example value")
            return False
        
        if not api_secret or api_secret == 'your_binance_api_secret_here':
            print("❌ BINANCE_API_SECRET not set or using example value")
            return False
        
        return True
    
    def print_config_summary(self) -> None:
        """Print a summary of the current configuration."""
        print("\n⚙️  Configuration Summary:")
        print(f"   API Key: {'✅ Set' if self.get_api_key() and self.get_api_key() != 'your_binance_api_key_here' else '❌ Not set'}")
        print(f"   API Secret: {'✅ Set' if self.get_api_secret() and self.get_api_secret() != 'your_binance_api_secret_here' else '❌ Not set'}")
        print(f"   Use Testnet: {self.use_testnet()}")
        print(f"   Business Service: {'Enabled' if self.enable_business_service() else 'Disabled'}")
        print(f"   Trading Symbols: {', '.join(self.get_trading_symbols())}")
        print(f"   Max Order Amount: ${self.get_max_order_amount()}")
        print(f"   Log Level: {self.get_log_level()}")

# Global config instance
config = ConfigLoader() 