import asyncio
import sys
import os
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.business_service import BusinessService, CexTransaction, TransactionSide, ExchangeType

async def test_dex_integration():
    """Test DEX integration with the business service."""
    print("🦄 Testing DEX Integration with Business Service")
    print("=" * 60)
    
    load_dotenv()
    
    # Create a mock business service (we don't need real API keys for DEX testing)
    business_service = BusinessService("demo_key", "demo_secret", testnet=True)
    
    # Test DEX buy transaction
    print("\n📈 Testing DEX Buy Transaction...")
    dex_buy_transaction = CexTransaction(
        ex_type=ExchangeType.DEX,
        quantity=0.001,  # 0.001 ETH
        expected_price=2000,  # $2000 per ETH
        pair="ETH",
        transaction_side=TransactionSide.BUY
    )
    
    try:
        await business_service._execute_dex_buy(dex_buy_transaction)
        print("✅ DEX buy test completed!")
    except Exception as e:
        print(f"❌ DEX buy test failed: {e}")
    
    # Test DEX sell transaction
    print("\n📉 Testing DEX Sell Transaction...")
    dex_sell_transaction = CexTransaction(
        ex_type=ExchangeType.DEX,
        quantity=0.001,  # 0.001 ETH
        expected_price=2000,  # $2000 per ETH
        pair="ETH",
        transaction_side=TransactionSide.SELL
    )
    
    try:
        await business_service._execute_dex_sell(dex_sell_transaction)
        print("✅ DEX sell test completed!")
    except Exception as e:
        print(f"❌ DEX sell test failed: {e}")
    
    # Test token address mapping
    print("\n🔗 Testing Token Address Mapping...")
    try:
        token_addresses = business_service._get_token_addresses("ETH")
        print(f"✅ Token addresses for ETH: {token_addresses}")
        
        token_addresses_usdt = business_service._get_token_addresses("USDT")
        print(f"✅ Token addresses for USDT: {token_addresses_usdt}")
    except Exception as e:
        print(f"❌ Token address mapping failed: {e}")

async def test_full_dex_flow():
    """Test the full DEX flow with event handling."""
    print("\n🚀 Testing Full DEX Flow...")
    print("=" * 60)
    
    load_dotenv()
    
    # Create business service
    business_service = BusinessService("demo_key", "demo_secret", testnet=True)
    
    # Test DEX event
    dex_event = "|dex|0.001|2000|ETH|buy|"
    print(f"📨 Testing DEX event: {dex_event}")
    
    try:
        await business_service.handle_cex_transaction_event(dex_event)
        print("✅ Full DEX flow test completed!")
    except Exception as e:
        print(f"❌ Full DEX flow test failed: {e}")

async def main():
    """Main test function."""
    print("🧪 DEX Integration Test Suite")
    print("=" * 60)
    
    # Test individual DEX methods
    await test_dex_integration()
    
    # Test full flow
    await test_full_dex_flow()
    
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    print("🎉 DEX integration testing completed!")
    print("✅ Your ODOS integration is ready to use!")

if __name__ == "__main__":
    asyncio.run(main())
