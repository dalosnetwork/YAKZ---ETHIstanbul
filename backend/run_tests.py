#!/usr/bin/env python3
import asyncio
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.business_service import BusinessService, CexTransaction, TransactionSide, ExchangeType
from unittest.mock import Mock

async def test_basic_functionality():
    """Test basic functionality."""
    print("�� Testing Basic Functionality...")
    print("=" * 50)
    
    # Test CexTransaction parsing
    event_data = "|cex|0.1|2000|ETH|buy|"
    transaction = CexTransaction.from_event_data(event_data)
    
    print(f"✅ Parsed transaction: {transaction.pair} {transaction.quantity} @ ${transaction.expected_price}")
    
    # Test business service with mocked client
    business_service = BusinessService("demo_key", "demo_secret", testnet=True)
    business_service.order_client = Mock()
    business_service.order_client.get_balance = Mock(return_value=10000.0)
    business_service.order_client.place_market_buy_order = Mock(return_value={"orderId": 12345})
    
    # Test event handling
    await business_service.handle_cex_transaction_event(event_data)
    
    print("✅ Basic functionality test passed!")

async def main():
    """Run tests."""
    print("🚀 Trading System Test Suite")
    print("=" * 60)
    
    await test_basic_functionality()
    
    print("\n🎉 All tests completed!")

if __name__ == "__main__":
    asyncio.run(main())
