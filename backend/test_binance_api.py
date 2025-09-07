#!/usr/bin/env python3
"""
Binance API Test Script

Bu script Binance API key'lerinin çalışıp çalışmadığını test eder.
"""

import asyncio
import sys
import os
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.order_client import BinanceOrderClient

async def test_binance_api():
    """Test Binance API connection and permissions."""
    print("🔑 Testing Binance API...")
    print("=" * 50)
    
    # Load .env file
    load_dotenv()
    
    # Get API credentials
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    
    if not api_key or not api_secret:
        print("❌ API credentials not found in .env file")
        return False
    
    print(f"✅ API Key: {api_key[:10]}...")
    print(f"✅ API Secret: {api_secret[:10]}...")
    
    try:
        # Create order client
        client = BinanceOrderClient(api_key, api_secret, testnet=True)
        print("✅ Order client created successfully")
        
        # Test 1: Get account info
        print("\n📊 Testing Account Info...")
        try:
            account_info = client.get_account_info()
            print("✅ Account info retrieved successfully")
            print(f"   Account type: {account_info.get('accountType', 'Unknown')}")
            print(f"   Can trade: {account_info.get('canTrade', False)}")
            print(f"   Can withdraw: {account_info.get('canWithdraw', False)}")
            print(f"   Can deposit: {account_info.get('canDeposit', False)}")
        except Exception as e:
            print(f"❌ Account info failed: {e}")
            return False
        
        # Test 2: Get balance
        print("\n💰 Testing Balance Check...")
        try:
            usdt_balance = client.get_balance('USDT')
            print(f"✅ USDT Balance: {usdt_balance}")
            
            btc_balance = client.get_balance('BTC')
            print(f"✅ BTC Balance: {btc_balance}")
        except Exception as e:
            print(f"❌ Balance check failed: {e}")
            return False
        
        # Test 3: Get symbol info
        print("\n📈 Testing Symbol Info...")
        try:
            symbol_info = client.get_symbol_info('BTCUSDT')
            print("✅ Symbol info retrieved successfully")
            print(f"   Symbol: {symbol_info.get('symbol')}")
            print(f"   Status: {symbol_info.get('status')}")
            print(f"   Base asset: {symbol_info.get('baseAsset')}")
            print(f"   Quote asset: {symbol_info.get('quoteAsset')}")
        except Exception as e:
            print(f"❌ Symbol info failed: {e}")
            return False
        
        # Test 4: Get open orders
        print("\n📋 Testing Open Orders...")
        try:
            open_orders = client.get_open_orders('BTCUSDT')
            print(f"✅ Open orders retrieved: {len(open_orders)} orders")
        except Exception as e:
            print(f"❌ Open orders failed: {e}")
            return False
        
        print("\n🎉 All Binance API tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Binance API test failed: {e}")
        return False

async def test_trading_system():
    """Test the complete trading system with real API."""
    print("\n🚀 Testing Trading System...")
    print("=" * 50)
    
    try:
        from src.business_service import BusinessService
        from unittest.mock import Mock
        
        # Load .env
        load_dotenv()
        api_key = os.getenv('BINANCE_API_KEY')
        api_secret = os.getenv('BINANCE_API_SECRET')
        
        # Create business service with real API
        business_service = BusinessService(api_key, api_secret, testnet=True)
        print("✅ Business service created with real API")
        
        # Test event handling
        test_event = "|cex|0.001|2000|ETH|buy|"  # Very small amount for safety
        print(f"📨 Testing event: {test_event}")
        
        await business_service.handle_cex_transaction_event(test_event)
        print("✅ Event handling test completed")
        
        return True
        
    except Exception as e:
        print(f"❌ Trading system test failed: {e}")
        return False

async def main():
    """Main test function."""
    print("🧪 Binance API Comprehensive Test")
    print("=" * 60)
    
    # Test API connection
    api_ok = await test_binance_api()
    
    if api_ok:
        # Test trading system
        system_ok = await test_trading_system()
        
        print("\n" + "=" * 60)
        print("📊 Test Summary")
        print("=" * 60)
        
        if system_ok:
            print("🎉 Everything is working perfectly!")
            print("✅ Your Binance API is ready for trading!")
        else:
            print("⚠️  API works but trading system has issues.")
    else:
        print("❌ Binance API test failed.")
        print("📝 Please check your API credentials and permissions.")
    
    return api_ok

if __name__ == "__main__":
    asyncio.run(main())
