import signal
import sys
import asyncio
from config.settings import SUCCESS_MESSAGES

def setup_signal_handlers(websocket_client):
    """
    Set up signal handlers for graceful shutdown.
    
    Args:
        websocket_client: The WebSocket client instance to close on shutdown
    """
    def signal_handler(signum, frame):
        print(f"\n{SUCCESS_MESSAGES['SHUTDOWN']}")
        asyncio.create_task(websocket_client.close())
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

def print_startup_banner():
    """Print the application startup banner."""
    print("Binance WebSocket Depth Monitor")
    print("Monitoring depth channels for cryptocurrency pairs")
    print("Press Ctrl+C to exit")
    print("=" * 80)

def print_shutdown_message():
    """Print shutdown message."""
    print("\nExiting...")

def validate_symbols(symbols):
    """
    Validate that symbols are in the correct format.
    
    Args:
        symbols (list): List of trading symbols
        
    Returns:
        bool: True if all symbols are valid, False otherwise
    """
    if not symbols:
        return False
        
    for symbol in symbols:
        if not isinstance(symbol, str) or len(symbol) < 6:
            return False
            
    return True

def format_symbol_list(symbols):
    """
    Format symbols list for display.
    
    Args:
        symbols (list): List of trading symbols
        
    Returns:
        str: Formatted string of symbols
    """
    return ', '.join(symbols) 