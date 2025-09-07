import asyncio
import websockets
import json
from datetime import datetime
import sys
import os

# Add the parent directory to the path so we can import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import (
    BINANCE_WS_BASE_URL,
    COMBINED_STREAM_ENDPOINT,
    WS_PING_INTERVAL,
    MAX_DISPLAY_ORDERS,
    TIMESTAMP_FORMAT,
    MICROSECOND_TIMESTAMP_FORMAT,
    ERROR_MESSAGES,
    SUCCESS_MESSAGES
)

class BinanceWebSocket:
    """
    Binance WebSocket client for real-time market data streaming.
    
    This class handles the WebSocket connection to Binance's public API,
    manages ping/pong for connection maintenance, and processes incoming
    market depth data.
    """
    
    def __init__(self, symbols, stream_type='depth'):
        """
        Initialize the WebSocket client.
        
        Args:
            symbols (list): List of trading symbols to monitor
            stream_type (str): Type of stream to subscribe to (default: 'depth')
        """
        self.symbols = [symbol.lower() for symbol in symbols]
        self.stream_type = stream_type
        self.websocket = None
        self.running = True
        
    async def connect(self):
        """
        Connect to Binance WebSocket stream and start processing messages.
        
        Creates a combined stream URL for the specified symbols and stream type,
        establishes the WebSocket connection, and starts message handling.
        """
        # Create combined stream URL for depth channels
        streams = [f"{symbol}@{self.stream_type}" for symbol in self.symbols]
        stream_url = "/".join(streams)
        ws_url = f"{BINANCE_WS_BASE_URL}{COMBINED_STREAM_ENDPOINT.format(streams=stream_url)}"
        
        print(f"Connecting to: {ws_url}")
        print(f"Subscribing to {self.stream_type} channels for: {', '.join(self.symbols)}")
        print("-" * 80)
        
        try:
            self.websocket = await websockets.connect(ws_url)
            print(f"{SUCCESS_MESSAGES['CONNECTED']} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("-" * 80)
            
            # Start ping/pong handler
            asyncio.create_task(self.ping_pong_handler())
            
            # Start message handler
            await self.handle_messages()
            
        except Exception as e:
            print(f"{ERROR_MESSAGES['CONNECTION_FAILED']}: {e}")
            self.running = False
    
    async def ping_pong_handler(self):
        """
        Handle ping/pong to keep the WebSocket connection alive.
        
        Binance requires pong responses to ping frames to maintain the connection.
        This method sends a pong frame every WS_PING_INTERVAL seconds.
        """
        while self.running and self.websocket:
            try:
                # Send pong every WS_PING_INTERVAL seconds to keep connection alive
                await asyncio.sleep(WS_PING_INTERVAL)
                if self.websocket and self.websocket.open:
                    await self.websocket.pong()
            except Exception as e:
                print(f"{ERROR_MESSAGES['PING_PONG_ERROR']}: {e}")
                break
    
    async def handle_messages(self):
        """
        Handle incoming WebSocket messages and process market data.
        
        Processes incoming messages, parses JSON data, and displays
        formatted market depth information for each symbol.
        """
        try:
            async for message in self.websocket:
                if not self.running:
                    break
                    
                try:
                    data = json.loads(message)
                    
                    # Handle combined stream format
                    if 'stream' in data and 'data' in data:
                        await self._process_stream_data(data)
                    
                    # Handle raw stream format (fallback)
                    else:
                        print(f"Raw message: {data}")
                        
                except json.JSONDecodeError as e:
                    print(f"{ERROR_MESSAGES['JSON_DECODE_ERROR']}: {e}")
                    print(f"Raw message: {message}")
                    
        except websockets.exceptions.ConnectionClosed:
            print("WebSocket connection closed")
        except Exception as e:
            print(f"{ERROR_MESSAGES['MESSAGE_HANDLING_ERROR']}: {e}")
        finally:
            self.running = False
    
    async def _process_stream_data(self, data):
        """
        Process stream data from combined stream format.
        
        Args:
            data (dict): Parsed JSON data from WebSocket message
        """
        stream_name = data['stream']
        stream_data = data['data']
        
        # Extract symbol from stream name (e.g., "btcusdt@depth" -> "BTCUSDT")
        symbol = stream_name.split('@')[0].upper()
        
        # Process based on stream type
        if self.stream_type == 'depth':
            self._display_depth_data(symbol, stream_data)
        else:
            # Handle other stream types in the future
            print(f"Received {self.stream_type} data for {symbol}: {stream_data}")
    
    def _display_depth_data(self, symbol, depth_data):
        """
        Display formatted depth (order book) data.
        
        Args:
            symbol (str): Trading symbol (e.g., "BTCUSDT")
            depth_data (dict): Depth data from WebSocket message
        """
        print(f"\n[{datetime.now().strftime(TIMESTAMP_FORMAT)}] {symbol} Depth Update:")
        print(f"  Event Time: {datetime.fromtimestamp(depth_data.get('E', 0)/1000).strftime(MICROSECOND_TIMESTAMP_FORMAT)[:-3]}")
        print(f"  First Update ID: {depth_data.get('U', 'N/A')}")
        print(f"  Final Update ID: {depth_data.get('u', 'N/A')}")
        
        # Print bid updates
        if 'b' in depth_data and depth_data['b']:
            print("  Bids:")
            for bid in depth_data['b'][:MAX_DISPLAY_ORDERS]:  # Show top bids
                price, quantity = bid
                print(f"    {price} : {quantity}")
        
        # Print ask updates
        if 'a' in depth_data and depth_data['a']:
            print("  Asks:")
            for ask in depth_data['a'][:MAX_DISPLAY_ORDERS]:  # Show top asks
                price, quantity = ask
                print(f"    {price} : {quantity}")
        
        print("-" * 60)
    
    async def close(self):
        """
        Close the WebSocket connection gracefully.
        
        Sets the running flag to False and closes the WebSocket connection.
        """
        self.running = False
        if self.websocket:
            await self.websocket.close()
            print(f"\n{SUCCESS_MESSAGES['DISCONNECTED']}") 