#!/usr/bin/env python3
"""
Binance Order Management Examples

This file demonstrates how to use the Binance order management system
for placing various types of spot orders.

Note: This is for demonstration purposes. Do not run on mainnet without proper testing.
"""

import sys
import os
from typing import Optional

# Add the parent directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.order_client import BinanceOrderClient
from src.order_types import (
    create_market_buy_order,
    create_market_sell_order,
    create_limit_buy_order,
    create_limit_sell_order,
    OrderSide,
    TimeInForce,
    OrderResponse
)

class OrderExamples:
    """
    Example class demonstrating various order operations.
    """
    
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        """
        Initialize the order examples with API credentials.
        
        Args:
            api_key (str): Binance API key
            api_secret (str): Binance API secret
            testnet (bool): Whether to use testnet (default: True for safety)
        """
        self.client = BinanceOrderClient(api_key, api_secret, testnet)
        self.testnet = testnet
        
        # Print warning for mainnet usage
        if not testnet:
            print("⚠️  WARNING: Using MAINNET - Real money will be used!")
            print("⚠️  Make sure you understand what you're doing!")
        else:
            print("✅ Using TESTNET - Safe for testing")
    
    def check_account_balance(self, asset: str = 'USDT') -> float:
        """
        Check account balance for a specific asset.
        
        Args:
            asset (str): Asset to check balance for
            
        Returns:
            float: Available balance
        """
        try:
            balance = self.client.get_balance(asset)
            print(f"💰 {asset} Balance: {balance}")
            return balance
        except Exception as e:
            print(f"❌ Error checking balance: {e}")
            return 0.0
    
    def get_current_price(self, symbol: str) -> Optional[float]:
        """
        Get current price for a symbol (simulation - would use ticker API).
        
        Args:
            symbol (str): Trading symbol
            
        Returns:
            float: Current price (simulated)
        """
        # In a real implementation, you would call the ticker API
        # For demo purposes, using example prices
        example_prices = {
            'BTCUSDT': 43000.0,
            'ETHUSDT': 2500.0,
            'BNBUSDT': 300.0,
            'ADAUSDT': 0.50,
            'SOLUSDT': 100.0
        }
        
        price = example_prices.get(symbol.upper())
        if price:
            print(f"📊 Current {symbol} price: ${price}")
        
        return price
    
    def example_market_buy_order(self, symbol: str = 'BTCUSDT', usdt_amount: float = 50.0):
        """
        Example: Place a market buy order using USDT amount.
        
        Args:
            symbol (str): Trading symbol
            usdt_amount (float): Amount in USDT to spend
        """
        print(f"\n🛒 Example: Market BUY {symbol} with ${usdt_amount} USDT")
        
        try:
            # Check USDT balance first
            usdt_balance = self.check_account_balance('USDT')
            if usdt_balance < usdt_amount:
                print(f"❌ Insufficient USDT balance. Need: {usdt_amount}, Have: {usdt_balance}")
                return
            
            # Create market buy order
            order = create_market_buy_order(
                symbol=symbol,
                quote_order_qty=usdt_amount,
                client_order_id=f"market_buy_{symbol.lower()}_{int(time.time())}"
            )
            
            print(f"📝 Order Details: {order.to_api_params()}")
            
            # In a real scenario, you would execute the order:
            # response = self.client.place_market_buy_order(
            #     symbol=order.symbol,
            #     quote_order_qty=order.quote_order_qty
            # )
            # print(f"✅ Order placed successfully: {response}")
            
            print("✅ Market buy order created (not executed in demo)")
            
        except Exception as e:
            print(f"❌ Error creating market buy order: {e}")
    
    def example_market_sell_order(self, symbol: str = 'BTCUSDT', quantity: float = 0.001):
        """
        Example: Place a market sell order.
        
        Args:
            symbol (str): Trading symbol
            quantity (float): Quantity to sell
        """
        print(f"\n💰 Example: Market SELL {quantity} {symbol}")
        
        try:
            # Get base asset (e.g., BTC from BTCUSDT)
            base_asset = symbol.replace('USDT', '').replace('BUSD', '').replace('BNB', '')
            
            # Check balance for base asset
            balance = self.check_account_balance(base_asset)
            if balance < quantity:
                print(f"❌ Insufficient {base_asset} balance. Need: {quantity}, Have: {balance}")
                return
            
            # Create market sell order
            order = create_market_sell_order(
                symbol=symbol,
                quantity=quantity,
                client_order_id=f"market_sell_{symbol.lower()}_{int(time.time())}"
            )
            
            print(f"📝 Order Details: {order.to_api_params()}")
            
            # In a real scenario, you would execute the order:
            # response = self.client.place_market_sell_order(
            #     symbol=order.symbol,
            #     quantity=order.quantity
            # )
            # print(f"✅ Order placed successfully: {response}")
            
            print("✅ Market sell order created (not executed in demo)")
            
        except Exception as e:
            print(f"❌ Error creating market sell order: {e}")
    
    def example_limit_buy_order(self, symbol: str = 'BTCUSDT', quantity: float = 0.001, 
                               price_offset: float = -500.0):
        """
        Example: Place a limit buy order below current market price.
        
        Args:
            symbol (str): Trading symbol
            quantity (float): Quantity to buy
            price_offset (float): Price offset from current price
        """
        print(f"\n📋 Example: Limit BUY {quantity} {symbol}")
        
        try:
            # Get current price and calculate limit price
            current_price = self.get_current_price(symbol)
            if not current_price:
                print(f"❌ Could not get current price for {symbol}")
                return
            
            limit_price = current_price + price_offset
            order_value = quantity * limit_price
            
            print(f"💡 Current price: ${current_price}")
            print(f"💡 Limit price: ${limit_price} (${price_offset} offset)")
            print(f"💡 Order value: ${order_value:.2f}")
            
            # Check USDT balance
            usdt_balance = self.check_account_balance('USDT')
            if usdt_balance < order_value:
                print(f"❌ Insufficient USDT balance. Need: {order_value:.2f}, Have: {usdt_balance}")
                return
            
            # Create limit buy order
            order = create_limit_buy_order(
                symbol=symbol,
                quantity=quantity,
                price=limit_price,
                time_in_force=TimeInForce.GTC,
                client_order_id=f"limit_buy_{symbol.lower()}_{int(time.time())}"
            )
            
            print(f"📝 Order Details: {order.to_api_params()}")
            
            # In a real scenario, you would execute the order:
            # response = self.client.place_limit_buy_order(
            #     symbol=order.symbol,
            #     quantity=order.quantity,
            #     price=order.price,
            #     time_in_force=order.time_in_force.value
            # )
            # print(f"✅ Order placed successfully: {response}")
            
            print("✅ Limit buy order created (not executed in demo)")
            
        except Exception as e:
            print(f"❌ Error creating limit buy order: {e}")
    
    def example_limit_sell_order(self, symbol: str = 'BTCUSDT', quantity: float = 0.001, 
                                price_offset: float = 500.0):
        """
        Example: Place a limit sell order above current market price.
        
        Args:
            symbol (str): Trading symbol
            quantity (float): Quantity to sell
            price_offset (float): Price offset from current price
        """
        print(f"\n💹 Example: Limit SELL {quantity} {symbol}")
        
        try:
            # Get base asset and check balance
            base_asset = symbol.replace('USDT', '').replace('BUSD', '').replace('BNB', '')
            balance = self.check_account_balance(base_asset)
            if balance < quantity:
                print(f"❌ Insufficient {base_asset} balance. Need: {quantity}, Have: {balance}")
                return
            
            # Get current price and calculate limit price
            current_price = self.get_current_price(symbol)
            if not current_price:
                print(f"❌ Could not get current price for {symbol}")
                return
            
            limit_price = current_price + price_offset
            order_value = quantity * limit_price
            
            print(f"💡 Current price: ${current_price}")
            print(f"💡 Limit price: ${limit_price} (+${price_offset} offset)")
            print(f"💡 Order value: ${order_value:.2f}")
            
            # Create limit sell order
            order = create_limit_sell_order(
                symbol=symbol,
                quantity=quantity,
                price=limit_price,
                time_in_force=TimeInForce.GTC,
                client_order_id=f"limit_sell_{symbol.lower()}_{int(time.time())}"
            )
            
            print(f"📝 Order Details: {order.to_api_params()}")
            
            # In a real scenario, you would execute the order:
            # response = self.client.place_limit_sell_order(
            #     symbol=order.symbol,
            #     quantity=order.quantity,
            #     price=order.price,
            #     time_in_force=order.time_in_force.value
            # )
            # print(f"✅ Order placed successfully: {response}")
            
            print("✅ Limit sell order created (not executed in demo)")
            
        except Exception as e:
            print(f"❌ Error creating limit sell order: {e}")
    
    def example_get_orders(self, symbol: str = 'BTCUSDT'):
        """
        Example: Get open orders and order history.
        
        Args:
            symbol (str): Trading symbol
        """
        print(f"\n📊 Example: Get orders for {symbol}")
        
        try:
            # In a real scenario, you would call:
            # open_orders = self.client.get_open_orders(symbol)
            # order_history = self.client.get_order_history(symbol, limit=10)
            
            print("📋 Open orders:")
            print("   (Would show currently active orders)")
            
            print("📜 Recent order history:")
            print("   (Would show last 10 orders)")
            
            print("✅ Order information retrieved (demo)")
            
        except Exception as e:
            print(f"❌ Error getting orders: {e}")
    
    def run_all_examples(self):
        """Run all order examples."""
        print("🚀 Running Binance Order Management Examples")
        print("=" * 60)
        
        # Check account info
        print("\n📊 Account Information:")
        self.check_account_balance('USDT')
        self.check_account_balance('BTC')
        self.check_account_balance('ETH')
        
        # Market orders
        self.example_market_buy_order('BTCUSDT', 50.0)
        self.example_market_sell_order('BTCUSDT', 0.001)
        
        # Limit orders
        self.example_limit_buy_order('BTCUSDT', 0.001, -500.0)
        self.example_limit_sell_order('BTCUSDT', 0.001, 500.0)
        
        # Order management
        self.example_get_orders('BTCUSDT')
        
        print("\n" + "=" * 60)
        print("✅ All examples completed!")
        print("💡 To execute real orders, uncomment the API calls in each function")

def main():
    """
    Main function to run examples.
    
    Note: Replace with your actual API credentials for testing.
    """
    # Example API credentials (replace with real ones for testing)
    API_KEY = "your_api_key_here"
    API_SECRET = "your_api_secret_here"
    
    # Use testnet for safety
    USE_TESTNET = True
    
    if API_KEY == "your_api_key_here":
        print("⚠️  Please set your actual API credentials before running examples")
        print("🔧 Edit the API_KEY and API_SECRET variables in this file")
        return
    
    # Create examples instance and run
    examples = OrderExamples(API_KEY, API_SECRET, USE_TESTNET)
    examples.run_all_examples()

if __name__ == "__main__":
    import time
    main() 