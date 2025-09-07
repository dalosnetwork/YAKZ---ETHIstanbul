#!/usr/bin/env python3
"""
Order Placement Test

Bu script order placement'ı test eder ve minimum amount'ları bulur.
"""

import asyncio
import sys
import os
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.order_client import BinanceOrderClient

async def test_order_placement():
    """Test order placement with different amounts."""
    print("📊 Testing Order Placement...")
    print("=" * 50)
    
    # Load .env file
    load_dotenv()
    
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    
    client = BinanceOrderClient(api_key, api_secret, testnet=True)
    
    # Test different symbols and amounts
    test_cases = [
        ("BTCUSDT", 0.001, 50000),  # 0.001 BTC @ $50k
        ("ETHUSDT", 0.01, 2000),   # 0.01 ETH @ $2k
        ("ADAUSDT", 10, 0.5),      # 10 ADA @ $0.5
    ]
    
    for symbol, quantity, price in test_cases:
        print(f"\n🧪 Testing {symbol}: {quantity} @ ${price}")
        
        try:
            # Get symbol info first
            symbol_info = client.get_symbol_info(symbol)
            print(f"   Symbol status: {symbol_info.get('status')}")
            
            # Check filters
            filters = {f['filterType']: f for f in symbol_info.get('filters', [])}
            
            if 'LOT_SIZE' in filters:
                lot_size = filters['LOT_SIZE']
                min_qty = float(lot_size['minQty'])
                max_qty = float(lot_size['maxQty'])
                step_size = float(lot_size['stepSize'])
                print(f"   Min quantity: {min_qty}")
                print(f"   Max quantity: {max_qty}")
                print(f"   Step size: {step_size}")
                
                # Adjust quantity to meet requirements
                if quantity < min_qty:
                    quantity = min_qty
                    print(f"   Adjusted quantity to: {quantity}")
            
            if 'PRICE_FILTER' in filters:
                price_filter = filters['PRICE_FILTER']
                min_price = float(price_filter['minPrice'])
                max_price = float(price_filter['maxPrice'])
                tick_size = float(price_filter['tickSize'])
                print(f"   Min price: {min_price}")
                print(f"   Max price: {max_price}")
                print(f"   Tick size: {tick_size}")
            
            # Try to place a very small test order
            print(f"   Attempting to place order...")
            
            # Calculate USDT amount
            usdt_amount = quantity * price
            
            # Try market buy order
            response = client.place_market_buy_order(
                symbol=symbol,
                quote_order_qty=usdt_amount
            )
            
            print(f"   ✅ Order placed successfully!")
            print(f"   Order ID: {response.get('orderId')}")
            print(f"   Status: {response.get('status')}")
            
            # Cancel the order immediately
            try:
                cancel_response = client.cancel_order(
                    symbol=symbol,
                    order_id=response.get('orderId')
                )
                print(f"   ✅ Order cancelled successfully")
            except Exception as e:
                print(f"   ⚠️  Could not cancel order: {e}")
            
        except Exception as e:
            print(f"   ❌ Order failed: {e}")
            
            # Try to get more specific error info
            if "MIN_NOTIONAL" in str(e):
                print(f"   💡 Try increasing the order amount")
            elif "LOT_SIZE" in str(e):
                print(f"   💡 Check quantity step size")
            elif "PRICE_FILTER" in str(e):
                print(f"   💡 Check price tick size")

async def main():
    """Main test function."""
    print("🧪 Order Placement Test")
    print("=" * 60)
    
    await test_order_placement()
    
    print("\n" + "=" * 60)
    print("📊 Test Complete")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
