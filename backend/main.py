import asyncio
from src.websocket_client import BinanceWebSocket
from src.business_service import BusinessService
from src.config_loader import config
from src.utils import setup_signal_handlers, print_startup_banner, print_shutdown_message, validate_symbols
from config.settings import DEFAULT_STREAM_TYPE, ERROR_MESSAGES

async def main():
    """
    Main application function.
    
    Initializes the WebSocket client, business service, sets up signal handlers,
    and starts monitoring the configured cryptocurrency symbols.
    """
    # Print configuration summary
    config.print_config_summary()
    
    # Get symbols from config
    symbols = config.get_trading_symbols()
    
    # Validate symbols configuration
    if not validate_symbols(symbols):
        print(f"{ERROR_MESSAGES['UNEXPECTED_ERROR']}: Invalid symbols configuration")
        return
    
    # Create WebSocket instance
    binance_ws = BinanceWebSocket(symbols, DEFAULT_STREAM_TYPE)
    
    # Create Business Service instance if enabled and configured
    business_service = None
    business_task = None
    
    if config.enable_business_service():
        if config.validate_config():
            business_service = BusinessService(
                config.get_api_key(),
                config.get_api_secret(),
                config.use_testnet()
            )
        else:
            print("⚠️  Business service disabled due to missing API configuration")
            print("📝 Copy env.example to .env and add your API keys to enable trading")
    
    # Set up graceful shutdown handling
    setup_signal_handlers(binance_ws)
    
    try:
        # Start business service in background if enabled
        if business_service:
            business_task = asyncio.create_task(business_service.start())
        
        # Connect and start receiving data
        await binance_ws.connect()
        
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    finally:
        # Stop business service
        if business_service:
            business_service.stop()
        await binance_ws.close()

if __name__ == "__main__":
    # Print startup information
    print_startup_banner()
    
    try:
        # Run the main application
        asyncio.run(main())
    except KeyboardInterrupt:
        print_shutdown_message()
    except Exception as e:
        print(f"{ERROR_MESSAGES['UNEXPECTED_ERROR']}: {e}")
