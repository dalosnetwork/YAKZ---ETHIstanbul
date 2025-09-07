import hmac
import hashlib
import time
import requests
import json
from datetime import datetime
from typing import Dict, Optional, Union
import sys
import os

# Add the parent directory to the path so we can import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import (
    BINANCE_API_BASE_URL,
    API_ENDPOINTS,
    ORDER_TYPES,
    ORDER_SIDES,
    TIME_IN_FORCE,
    ORDER_STATUS,
    ERROR_MESSAGES,
    SUCCESS_MESSAGES
)

class BinanceOrderClient:
    """
    Binance Spot Trading API client for placing buy and sell orders.
    
    This class handles authentication, order placement, and order management
    for Binance spot trading using REST API.
    """
    
    def __init__(self, api_key: str, api_secret: str, testnet: bool = False):
        """
        Initialize the Binance order client.
        
        Args:
            api_key (str): Binance API key
            api_secret (str): Binance API secret
            testnet (bool): Whether to use testnet (default: False)
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = BINANCE_API_BASE_URL['TESTNET'] if testnet else BINANCE_API_BASE_URL['MAINNET']
        self.session = requests.Session()
        self.session.headers.update({
            'X-MBX-APIKEY': self.api_key,
            'Content-Type': 'application/json'
        })
    
    def _generate_signature(self, query_string: str) -> str:
        """
        Generate HMAC SHA256 signature for API authentication.
        
        Args:
            query_string (str): Query string to sign
            
        Returns:
            str: Generated signature
        """
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    def _make_request(self, method: str, endpoint: str, params: Dict = None, signed: bool = True) -> Dict:
        """
        Make authenticated request to Binance API.
        
        Args:
            method (str): HTTP method (GET, POST, DELETE)
            endpoint (str): API endpoint
            params (dict): Request parameters
            signed (bool): Whether the request needs to be signed
            
        Returns:
            dict: API response
        """
        if params is None:
            params = {}
        
        url = f"{self.base_url}{endpoint}"
        
        if signed:
            # Add timestamp
            params['timestamp'] = int(time.time() * 1000)
            
            # Create query string
            query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
            
            # Generate signature
            signature = self._generate_signature(query_string)
            params['signature'] = signature
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, params=params)
            elif method.upper() == 'POST':
                response = self.session.post(url, params=params)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, params=params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to decode API response: {str(e)}")
    
    def get_account_info(self) -> Dict:
        """
        Get account information including balances.
        
        Returns:
            dict: Account information
        """
        try:
            return self._make_request('GET', API_ENDPOINTS['ACCOUNT'])
        except Exception as e:
            raise Exception(f"Failed to get account info: {str(e)}")
    
    def get_symbol_info(self, symbol: str) -> Dict:
        """
        Get trading rules and symbol information.
        
        Args:
            symbol (str): Trading symbol (e.g., 'BTCUSDT')
            
        Returns:
            dict: Symbol information
        """
        try:
            response = self._make_request('GET', API_ENDPOINTS['EXCHANGE_INFO'], signed=False)
            symbols = response.get('symbols', [])
            
            for symbol_info in symbols:
                if symbol_info['symbol'] == symbol.upper():
                    return symbol_info
            
            raise Exception(f"Symbol {symbol} not found")
        except Exception as e:
            raise Exception(f"Failed to get symbol info: {str(e)}")
    
    def place_market_buy_order(self, symbol: str, quantity: Optional[float] = None, 
                              quote_order_qty: Optional[float] = None) -> Dict:
        """
        Place a market buy order.
        
        Args:
            symbol (str): Trading symbol (e.g., 'BTCUSDT')
            quantity (float, optional): Quantity to buy
            quote_order_qty (float, optional): Quote asset quantity (USDT amount)
            
        Returns:
            dict: Order response
        """
        if not quantity and not quote_order_qty:
            raise ValueError("Either quantity or quote_order_qty must be specified")
        
        params = {
            'symbol': symbol.upper(),
            'side': ORDER_SIDES['BUY'],
            'type': ORDER_TYPES['MARKET']
        }
        
        if quantity:
            params['quantity'] = quantity
        if quote_order_qty:
            params['quoteOrderQty'] = quote_order_qty
        
        try:
            response = self._make_request('POST', API_ENDPOINTS['ORDER'], params)
            print(f"{SUCCESS_MESSAGES['ORDER_PLACED']}: Market BUY {symbol}")
            return response
        except Exception as e:
            raise Exception(f"Failed to place market buy order: {str(e)}")
    
    def place_market_sell_order(self, symbol: str, quantity: float) -> Dict:
        """
        Place a market sell order.
        
        Args:
            symbol (str): Trading symbol (e.g., 'BTCUSDT')
            quantity (float): Quantity to sell
            
        Returns:
            dict: Order response
        """
        params = {
            'symbol': symbol.upper(),
            'side': ORDER_SIDES['SELL'],
            'type': ORDER_TYPES['MARKET'],
            'quantity': quantity
        }
        
        try:
            response = self._make_request('POST', API_ENDPOINTS['ORDER'], params)
            print(f"{SUCCESS_MESSAGES['ORDER_PLACED']}: Market SELL {symbol}")
            return response
        except Exception as e:
            raise Exception(f"Failed to place market sell order: {str(e)}")
    
    def place_limit_buy_order(self, symbol: str, quantity: float, price: float, 
                             time_in_force: str = 'GTC') -> Dict:
        """
        Place a limit buy order.
        
        Args:
            symbol (str): Trading symbol (e.g., 'BTCUSDT')
            quantity (float): Quantity to buy
            price (float): Limit price
            time_in_force (str): Time in force (GTC, IOC, FOK)
            
        Returns:
            dict: Order response
        """
        params = {
            'symbol': symbol.upper(),
            'side': ORDER_SIDES['BUY'],
            'type': ORDER_TYPES['LIMIT'],
            'quantity': quantity,
            'price': price,
            'timeInForce': time_in_force
        }
        
        try:
            response = self._make_request('POST', API_ENDPOINTS['ORDER'], params)
            print(f"{SUCCESS_MESSAGES['ORDER_PLACED']}: Limit BUY {symbol} @ {price}")
            return response
        except Exception as e:
            raise Exception(f"Failed to place limit buy order: {str(e)}")
    
    def place_limit_sell_order(self, symbol: str, quantity: float, price: float, 
                              time_in_force: str = 'GTC') -> Dict:
        """
        Place a limit sell order.
        
        Args:
            symbol (str): Trading symbol (e.g., 'BTCUSDT')
            quantity (float): Quantity to sell
            price (float): Limit price
            time_in_force (str): Time in force (GTC, IOC, FOK)
            
        Returns:
            dict: Order response
        """
        params = {
            'symbol': symbol.upper(),
            'side': ORDER_SIDES['SELL'],
            'type': ORDER_TYPES['LIMIT'],
            'quantity': quantity,
            'price': price,
            'timeInForce': time_in_force
        }
        
        try:
            response = self._make_request('POST', API_ENDPOINTS['ORDER'], params)
            print(f"{SUCCESS_MESSAGES['ORDER_PLACED']}: Limit SELL {symbol} @ {price}")
            return response
        except Exception as e:
            raise Exception(f"Failed to place limit sell order: {str(e)}")
    
    def cancel_order(self, symbol: str, order_id: Optional[int] = None, 
                    orig_client_order_id: Optional[str] = None) -> Dict:
        """
        Cancel an existing order.
        
        Args:
            symbol (str): Trading symbol
            order_id (int, optional): Order ID
            orig_client_order_id (str, optional): Client order ID
            
        Returns:
            dict: Cancel response
        """
        if not order_id and not orig_client_order_id:
            raise ValueError("Either order_id or orig_client_order_id must be specified")
        
        params = {'symbol': symbol.upper()}
        
        if order_id:
            params['orderId'] = order_id
        if orig_client_order_id:
            params['origClientOrderId'] = orig_client_order_id
        
        try:
            response = self._make_request('DELETE', API_ENDPOINTS['ORDER'], params)
            print(f"{SUCCESS_MESSAGES['ORDER_CANCELLED']}: {symbol}")
            return response
        except Exception as e:
            raise Exception(f"Failed to cancel order: {str(e)}")
    
    def get_order_status(self, symbol: str, order_id: Optional[int] = None, 
                        orig_client_order_id: Optional[str] = None) -> Dict:
        """
        Get order status.
        
        Args:
            symbol (str): Trading symbol
            order_id (int, optional): Order ID
            orig_client_order_id (str, optional): Client order ID
            
        Returns:
            dict: Order status
        """
        if not order_id and not orig_client_order_id:
            raise ValueError("Either order_id or orig_client_order_id must be specified")
        
        params = {'symbol': symbol.upper()}
        
        if order_id:
            params['orderId'] = order_id
        if orig_client_order_id:
            params['origClientOrderId'] = orig_client_order_id
        
        try:
            return self._make_request('GET', API_ENDPOINTS['ORDER'], params)
        except Exception as e:
            raise Exception(f"Failed to get order status: {str(e)}")
    
    def get_open_orders(self, symbol: Optional[str] = None) -> Dict:
        """
        Get all open orders.
        
        Args:
            symbol (str, optional): Trading symbol (if None, gets all symbols)
            
        Returns:
            dict: Open orders
        """
        params = {}
        if symbol:
            params['symbol'] = symbol.upper()
        
        try:
            return self._make_request('GET', API_ENDPOINTS['OPEN_ORDERS'], params)
        except Exception as e:
            raise Exception(f"Failed to get open orders: {str(e)}")
    
    def get_order_history(self, symbol: str, limit: int = 500) -> Dict:
        """
        Get order history for a symbol.
        
        Args:
            symbol (str): Trading symbol
            limit (int): Number of orders to retrieve (max 1000)
            
        Returns:
            dict: Order history
        """
        params = {
            'symbol': symbol.upper(),
            'limit': min(limit, 1000)
        }
        
        try:
            return self._make_request('GET', API_ENDPOINTS['ALL_ORDERS'], params)
        except Exception as e:
            raise Exception(f"Failed to get order history: {str(e)}")
    
    def get_balance(self, asset: str) -> float:
        """
        Get balance for a specific asset.
        
        Args:
            asset (str): Asset symbol (e.g., 'BTC', 'USDT')
            
        Returns:
            float: Available balance
        """
        try:
            account_info = self.get_account_info()
            balances = account_info.get('balances', [])
            
            for balance in balances:
                if balance['asset'] == asset.upper():
                    return float(balance['free'])
            
            return 0.0
        except Exception as e:
            raise Exception(f"Failed to get balance for {asset}: {str(e)}")
    
    def validate_order_params(self, symbol: str, quantity: float, price: Optional[float] = None) -> bool:
        """
        Validate order parameters against symbol trading rules.
        
        Args:
            symbol (str): Trading symbol
            quantity (float): Order quantity
            price (float, optional): Order price (for limit orders)
            
        Returns:
            bool: True if valid, raises exception if invalid
        """
        try:
            symbol_info = self.get_symbol_info(symbol)
            filters = {f['filterType']: f for f in symbol_info['filters']}
            
            # Check LOT_SIZE filter
            if 'LOT_SIZE' in filters:
                lot_size = filters['LOT_SIZE']
                min_qty = float(lot_size['minQty'])
                max_qty = float(lot_size['maxQty'])
                step_size = float(lot_size['stepSize'])
                
                if quantity < min_qty:
                    raise ValueError(f"Quantity {quantity} is below minimum {min_qty}")
                if quantity > max_qty:
                    raise ValueError(f"Quantity {quantity} is above maximum {max_qty}")
                
                # Check step size
                if step_size > 0:
                    remainder = (quantity - min_qty) % step_size
                    if abs(remainder) > 1e-8:  # Allow for floating point precision
                        raise ValueError(f"Quantity {quantity} does not match step size {step_size}")
            
            # Check PRICE_FILTER if price is provided
            if price and 'PRICE_FILTER' in filters:
                price_filter = filters['PRICE_FILTER']
                min_price = float(price_filter['minPrice'])
                max_price = float(price_filter['maxPrice'])
                tick_size = float(price_filter['tickSize'])
                
                if price < min_price:
                    raise ValueError(f"Price {price} is below minimum {min_price}")
                if price > max_price:
                    raise ValueError(f"Price {price} is above maximum {max_price}")
                
                # Check tick size
                if tick_size > 0:
                    remainder = (price - min_price) % tick_size
                    if abs(remainder) > 1e-8:  # Allow for floating point precision
                        raise ValueError(f"Price {price} does not match tick size {tick_size}")
            
            return True
            
        except Exception as e:
            raise Exception(f"Order validation failed: {str(e)}") 