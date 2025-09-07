#!/usr/bin/env python3
"""
Comprehensive Test Suite

This file contains comprehensive tests for the trading system.
"""

import asyncio
import sys
import os
from unittest.mock import Mock, patch, AsyncMock

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.business_service import BusinessService, CexTransaction, TransactionSide, ExchangeType

class ComprehensiveTestSuite:
    """Comprehensive test suite for the trading system."""
    
    def __init__(self):
        self.business_service = None
        self.test_results = []
    
    async def setup_test_environment(self):
        """Set up test environment with mocked APIs."""
        print("🔧 Setting up Test Environment...")
        
        # Create business service with demo credentials
        self.business_service = BusinessService("test_key", "test_secret", testnet=True)
        
        # Mock the order client to prevent real API calls
        self.business_service.order_client = Mock()
        self.business_service.order_client.get_balance = Mock(return_value=10000.0)
        self.business_service.order_client.place_market_buy_order = Mock(return_value={"orderId": 12345})
        self.business_service.order_client.place_market_sell_order = Mock(return_value={"orderId": 12346})
        
        print("✅ Test environment ready!")
    
    async def test_transaction_parsing(self):
        """Test transaction parsing with various formats."""
        print("\n📝 Testing Transaction Parsing...")
        print("=" * 50)
        
        test_cases = [
            ("CEX Buy", "|cex|0.1|2000|ETH|buy|"),
            ("CEX Sell", "|cex|0.5|1000|BTC|sell|"),
            ("DEX Buy", "|dex|1.0|50|SOL|buy|"),
            ("DEX Sell", "|dex|1000.0|0.5|ADA|sell|"),
        ]
        
        for name, event_data in test_cases:
            try:
                transaction = CexTransaction.from_event_data(event_data)
                print(f"✅ {name}: {transaction.pair} {transaction.quantity} @ ${transaction.expected_price}")
                self.test_results.append((name, True))
            except Exception as e:
                print(f"❌ {name}: {e}")
                self.test_results.append((name, False))
    
    async def test_risk_management(self):
        """Test risk management scenarios."""
        print("\n🛡️ Testing Risk Management...")
        print("=" * 50)
        
        # Test scenarios
        risk_tests = [
            ("Normal trade", "|cex|0.1|2000|ETH|buy|", True),
            ("Too small trade", "|cex|0.0001|2000|ETH|buy|", False),
            ("Large trade", "|cex|100|2000|ETH|buy|", False),
            ("Invalid format", "invalid_data", False),
        ]
        
        for name, event_data, should_pass in risk_tests:
            try:
                await self.business_service.handle_cex_transaction_event(event_data)
                if should_pass:
                    print(f"✅ {name}: Passed as expected")
                    self.test_results.append((name, True))
                else:
                    print(f"❌ {name}: Should have failed but passed")
                    self.test_results.append((name, False))
            except Exception as e:
                if not should_pass:
                    print(f"✅ {name}: Failed as expected - {e}")
                    self.test_results.append((name, True))
                else:
                    print(f"❌ {name}: Should have passed but failed - {e}")
                    self.test_results.append((name, False))
    
    async def test_cex_execution(self):
        """Test CEX execution scenarios."""
        print("\n🏦 Testing CEX Execution...")
        print("=" * 50)
        
        cex_tests = [
            ("CEX Buy", "|cex|0.1|2000|ETH|buy|"),
            ("CEX Sell", "|cex|0.5|1000|BTC|sell|"),
        ]
        
        for name, event_data in cex_tests:
            try:
                await self.business_service.handle_cex_transaction_event(event_data)
                print(f"✅ {name}: Executed successfully")
                self.test_results.append((name, True))
            except Exception as e:
                print(f"❌ {name}: Failed - {e}")
                self.test_results.append((name, False))
    
    async def test_dex_execution(self):
        """Test DEX execution scenarios."""
        print("\n🦄 Testing DEX Execution...")
        print("=" * 50)
        
        dex_tests = [
            ("DEX Buy", "|dex|1.0|50|SOL|buy|"),
            ("DEX Sell", "|dex|1000.0|0.5|ADA|sell|"),
        ]
        
        for name, event_data in dex_tests:
            try:
                await self.business_service.handle_cex_transaction_event(event_data)
                print(f"✅ {name}: Executed successfully")
                self.test_results.append((name, True))
            except Exception as e:
                print(f"❌ {name}: Failed - {e}")
                self.test_results.append((name, False))
    
    async def test_contract_event_handling(self):
        """Test contract event handling."""
        print("\n�� Testing Contract Event Handling...")
        print("=" * 50)
        
        # Simulate contract events
        contract_events = [
            {
                'address': '0x1234567890123456789012345678901234567890',
                'blockNumber': 12345,
                'transactionHash': '0xabcdef1234567890',
                'args': {
                    'exType': 'cex',
                    'quantity': 1000000000000000000,  # 1 ETH in wei
                    'expectedPrice': 2000000000000000000000,  # 2000 USDT in wei
                    'pair': 'ETH',
                    'side': 'buy'
                }
            }
        ]
        
        for event in contract_events:
            try:
                print(f"📨 Processing contract event: {event['transactionHash']}")
                await self.business_service._handle_contract_event(event)
                print(f"✅ Contract event processed successfully")
                self.test_results.append(("Contract Event", True))
            except Exception as e:
                print(f"❌ Contract event failed: {e}")
                self.test_results.append(("Contract Event", False))
    
    async def test_error_handling(self):
        """Test error handling scenarios."""
        print("\n⚠️ Testing Error Handling...")
        print("=" * 50)
        
        error_tests = [
            ("Invalid event format", "invalid_data"),
            ("Missing fields", "|cex|0.1|2000|ETH|"),
            ("Invalid exchange type", "|invalid|0.1|2000|ETH|buy|"),
            ("Invalid transaction side", "|cex|0.1|2000|ETH|invalid|"),
        ]
        
        for name, event_data in error_tests:
            try:
                await self.business_service.handle_cex_transaction_event(event_data)
                print(f"❌ {name}: Should have failed but passed")
                self.test_results.append((name, False))
            except Exception as e:
                print(f"✅ {name}: Failed as expected - {e}")
                self.test_results.append((name, True))
    
    async def run_all_tests(self):
        """Run all comprehensive tests."""
        print("🚀 Starting Comprehensive Test Suite")
        print("=" * 60)
        
        await self.setup_test_environment()
        await self.test_transaction_parsing()
        await self.test_risk_management()
        await self.test_cex_execution()
        await self.test_dex_execution()
        await self.test_contract_event_handling()
        await self.test_error_handling()
        
        # Print summary
        print("\n" + "="*60)
        print("📊 Test Summary")
        print("="*60)
        
        passed = sum(1 for _, result in self.test_results if result)
        total = len(self.test_results)
        
        for test_name, result in self.test_results:
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"{test_name}: {status}")
        
        print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if passed == total:
            print("🎉 All tests passed! System is ready for deployment.")
        else:
            print("⚠️  Some tests failed. Please check the errors above.")
        
        return passed == total

async def main():
    """Run comprehensive tests."""
    test_suite = ComprehensiveTestSuite()
    success = await test_suite.run_all_tests()
    return success

if __name__ == "__main__":
    asyncio.run(main())
