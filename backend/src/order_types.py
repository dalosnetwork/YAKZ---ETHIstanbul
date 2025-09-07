from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum
import sys
import os

# Add the parent directory to the path so we can import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import ORDER_TYPES, ORDER_SIDES, TIME_IN_FORCE, ORDER_STATUS

class OrderSide(Enum):
    """Order side enumeration."""
    BUY = ORDER_SIDES['BUY']
    SELL = ORDER_SIDES['SELL']

class OrderType(Enum):
    """Order type enumeration."""
    LIMIT = ORDER_TYPES['LIMIT']
    MARKET = ORDER_TYPES['MARKET']
    STOP_LOSS = ORDER_TYPES['STOP_LOSS']
    STOP_LOSS_LIMIT = ORDER_TYPES['STOP_LOSS_LIMIT']
    TAKE_PROFIT = ORDER_TYPES['TAKE_PROFIT']
    TAKE_PROFIT_LIMIT = ORDER_TYPES['TAKE_PROFIT_LIMIT']
    LIMIT_MAKER = ORDER_TYPES['LIMIT_MAKER']

class TimeInForce(Enum):
    """Time in force enumeration."""
    GTC = TIME_IN_FORCE['GTC']  # Good Till Cancelled
    IOC = TIME_IN_FORCE['IOC']  # Immediate or Cancel
    FOK = TIME_IN_FORCE['FOK']  # Fill or Kill

class OrderStatus(Enum):
    """Order status enumeration."""
    NEW = ORDER_STATUS['NEW']
    PARTIALLY_FILLED = ORDER_STATUS['PARTIALLY_FILLED']
    FILLED = ORDER_STATUS['FILLED']
    CANCELED = ORDER_STATUS['CANCELED']
    PENDING_CANCEL = ORDER_STATUS['PENDING_CANCEL']
    REJECTED = ORDER_STATUS['REJECTED']
    EXPIRED = ORDER_STATUS['EXPIRED']

@dataclass
class BaseOrder:
    """Base order class with common fields."""
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: Optional[float] = None
    quote_order_qty: Optional[float] = None
    client_order_id: Optional[str] = None
    
    def __post_init__(self):
        """Validate order after initialization."""
        self.symbol = self.symbol.upper()
        self.validate()
    
    def validate(self) -> bool:
        """
        Validate basic order parameters.
        
        Returns:
            bool: True if valid
            
        Raises:
            ValueError: If validation fails
        """
        if not self.symbol:
            raise ValueError("Symbol is required")
        
        if not isinstance(self.side, OrderSide):
            raise ValueError("Invalid order side")
        
        if not isinstance(self.order_type, OrderType):
            raise ValueError("Invalid order type")
        
        if not self.quantity and not self.quote_order_qty:
            raise ValueError("Either quantity or quote_order_qty must be specified")
        
        if self.quantity and self.quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        if self.quote_order_qty and self.quote_order_qty <= 0:
            raise ValueError("Quote order quantity must be positive")
        
        return True
    
    def to_api_params(self) -> Dict[str, Any]:
        """
        Convert order to API parameters.
        
        Returns:
            dict: API parameters
        """
        params = {
            'symbol': self.symbol,
            'side': self.side.value,
            'type': self.order_type.value
        }
        
        if self.quantity:
            params['quantity'] = self.quantity
        
        if self.quote_order_qty:
            params['quoteOrderQty'] = self.quote_order_qty
        
        if self.client_order_id:
            params['newClientOrderId'] = self.client_order_id
        
        return params

@dataclass
class MarketOrder(BaseOrder):
    """Market order class."""
    
    def __init__(self, symbol: str, side: OrderSide, quantity: Optional[float] = None, 
                 quote_order_qty: Optional[float] = None, client_order_id: Optional[str] = None):
        super().__init__(
            symbol=symbol,
            side=side,
            order_type=OrderType.MARKET,
            quantity=quantity,
            quote_order_qty=quote_order_qty,
            client_order_id=client_order_id
        )

@dataclass
class LimitOrder(BaseOrder):
    """Limit order class."""
    price: float
    time_in_force: TimeInForce = TimeInForce.GTC
    
    def __init__(self, symbol: str, side: OrderSide, quantity: float, price: float,
                 time_in_force: TimeInForce = TimeInForce.GTC, client_order_id: Optional[str] = None):
        self.price = price
        self.time_in_force = time_in_force
        super().__init__(
            symbol=symbol,
            side=side,
            order_type=OrderType.LIMIT,
            quantity=quantity,
            client_order_id=client_order_id
        )
    
    def validate(self) -> bool:
        """
        Validate limit order parameters.
        
        Returns:
            bool: True if valid
            
        Raises:
            ValueError: If validation fails
        """
        super().validate()
        
        if self.price <= 0:
            raise ValueError("Price must be positive")
        
        if not isinstance(self.time_in_force, TimeInForce):
            raise ValueError("Invalid time in force")
        
        return True
    
    def to_api_params(self) -> Dict[str, Any]:
        """
        Convert limit order to API parameters.
        
        Returns:
            dict: API parameters
        """
        params = super().to_api_params()
        params['price'] = self.price
        params['timeInForce'] = self.time_in_force.value
        return params

@dataclass
class StopLossOrder(BaseOrder):
    """Stop loss order class."""
    stop_price: float
    
    def __init__(self, symbol: str, side: OrderSide, quantity: float, stop_price: float,
                 client_order_id: Optional[str] = None):
        self.stop_price = stop_price
        super().__init__(
            symbol=symbol,
            side=side,
            order_type=OrderType.STOP_LOSS,
            quantity=quantity,
            client_order_id=client_order_id
        )
    
    def validate(self) -> bool:
        """
        Validate stop loss order parameters.
        
        Returns:
            bool: True if valid
            
        Raises:
            ValueError: If validation fails
        """
        super().validate()
        
        if self.stop_price <= 0:
            raise ValueError("Stop price must be positive")
        
        return True
    
    def to_api_params(self) -> Dict[str, Any]:
        """
        Convert stop loss order to API parameters.
        
        Returns:
            dict: API parameters
        """
        params = super().to_api_params()
        params['stopPrice'] = self.stop_price
        return params

@dataclass
class StopLossLimitOrder(BaseOrder):
    """Stop loss limit order class."""
    price: float
    stop_price: float
    time_in_force: TimeInForce = TimeInForce.GTC
    
    def __init__(self, symbol: str, side: OrderSide, quantity: float, price: float, 
                 stop_price: float, time_in_force: TimeInForce = TimeInForce.GTC,
                 client_order_id: Optional[str] = None):
        self.price = price
        self.stop_price = stop_price
        self.time_in_force = time_in_force
        super().__init__(
            symbol=symbol,
            side=side,
            order_type=OrderType.STOP_LOSS_LIMIT,
            quantity=quantity,
            client_order_id=client_order_id
        )
    
    def validate(self) -> bool:
        """
        Validate stop loss limit order parameters.
        
        Returns:
            bool: True if valid
            
        Raises:
            ValueError: If validation fails
        """
        super().validate()
        
        if self.price <= 0:
            raise ValueError("Price must be positive")
        
        if self.stop_price <= 0:
            raise ValueError("Stop price must be positive")
        
        if not isinstance(self.time_in_force, TimeInForce):
            raise ValueError("Invalid time in force")
        
        return True
    
    def to_api_params(self) -> Dict[str, Any]:
        """
        Convert stop loss limit order to API parameters.
        
        Returns:
            dict: API parameters
        """
        params = super().to_api_params()
        params['price'] = self.price
        params['stopPrice'] = self.stop_price
        params['timeInForce'] = self.time_in_force.value
        return params

@dataclass
class OrderResponse:
    """Order response class for handling API responses."""
    symbol: str
    order_id: int
    client_order_id: str
    status: OrderStatus
    side: OrderSide
    order_type: OrderType
    quantity: float
    filled_quantity: float
    price: Optional[float] = None
    stop_price: Optional[float] = None
    time_in_force: Optional[TimeInForce] = None
    order_time: Optional[int] = None
    update_time: Optional[int] = None
    
    @classmethod
    def from_api_response(cls, response: Dict[str, Any]) -> 'OrderResponse':
        """
        Create OrderResponse from API response.
        
        Args:
            response (dict): API response data
            
        Returns:
            OrderResponse: Order response object
        """
        return cls(
            symbol=response['symbol'],
            order_id=response['orderId'],
            client_order_id=response['clientOrderId'],
            status=OrderStatus(response['status']),
            side=OrderSide(response['side']),
            order_type=OrderType(response['type']),
            quantity=float(response['origQty']),
            filled_quantity=float(response['executedQty']),
            price=float(response['price']) if response.get('price') else None,
            stop_price=float(response['stopPrice']) if response.get('stopPrice') else None,
            time_in_force=TimeInForce(response['timeInForce']) if response.get('timeInForce') else None,
            order_time=response.get('transactTime'),
            update_time=response.get('updateTime')
        )
    
    def is_filled(self) -> bool:
        """Check if order is completely filled."""
        return self.status == OrderStatus.FILLED
    
    def is_partially_filled(self) -> bool:
        """Check if order is partially filled."""
        return self.status == OrderStatus.PARTIALLY_FILLED
    
    def is_active(self) -> bool:
        """Check if order is still active."""
        return self.status in [OrderStatus.NEW, OrderStatus.PARTIALLY_FILLED]
    
    def remaining_quantity(self) -> float:
        """Get remaining quantity to be filled."""
        return self.quantity - self.filled_quantity

def create_market_buy_order(symbol: str, quantity: Optional[float] = None, 
                           quote_order_qty: Optional[float] = None, 
                           client_order_id: Optional[str] = None) -> MarketOrder:
    """
    Create a market buy order.
    
    Args:
        symbol (str): Trading symbol
        quantity (float, optional): Quantity to buy
        quote_order_qty (float, optional): Quote asset quantity
        client_order_id (str, optional): Client order ID
        
    Returns:
        MarketOrder: Market buy order
    """
    return MarketOrder(symbol, OrderSide.BUY, quantity, quote_order_qty, client_order_id)

def create_market_sell_order(symbol: str, quantity: float, 
                            client_order_id: Optional[str] = None) -> MarketOrder:
    """
    Create a market sell order.
    
    Args:
        symbol (str): Trading symbol
        quantity (float): Quantity to sell
        client_order_id (str, optional): Client order ID
        
    Returns:
        MarketOrder: Market sell order
    """
    return MarketOrder(symbol, OrderSide.SELL, quantity, None, client_order_id)

def create_limit_buy_order(symbol: str, quantity: float, price: float,
                          time_in_force: TimeInForce = TimeInForce.GTC,
                          client_order_id: Optional[str] = None) -> LimitOrder:
    """
    Create a limit buy order.
    
    Args:
        symbol (str): Trading symbol
        quantity (float): Quantity to buy
        price (float): Limit price
        time_in_force (TimeInForce): Time in force
        client_order_id (str, optional): Client order ID
        
    Returns:
        LimitOrder: Limit buy order
    """
    return LimitOrder(symbol, OrderSide.BUY, quantity, price, time_in_force, client_order_id)

def create_limit_sell_order(symbol: str, quantity: float, price: float,
                           time_in_force: TimeInForce = TimeInForce.GTC,
                           client_order_id: Optional[str] = None) -> LimitOrder:
    """
    Create a limit sell order.
    
    Args:
        symbol (str): Trading symbol
        quantity (float): Quantity to sell
        price (float): Limit price
        time_in_force (TimeInForce): Time in force
        client_order_id (str, optional): Client order ID
        
    Returns:
        LimitOrder: Limit sell order
    """
    return LimitOrder(symbol, OrderSide.SELL, quantity, price, time_in_force, client_order_id) 