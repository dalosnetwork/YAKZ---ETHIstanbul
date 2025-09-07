#!/usr/bin/env python3
"""
CexTransaction Event Example

This example demonstrates how to use the updated BusinessService
to handle CexTransaction events with the specified data format.
"""

import asyncio
import sys
import os

# Add the parent directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.business_service import BusinessService

async def main():
    """Demonstrate CexTransaction event handling."""
    print("🎯 CexTransaction Event Handling Example")
    print("=" * 50)
    
    # Initialize business service (using demo credentials)
    business_service = BusinessService("demo_key", "demo_secret", testnet=True)
    
    # Example CexTransaction events
    example_events = [
        "|cex|4200|0.5|ETH|buy|",      # CEX buy 0.5 ETH for $4200
        "|dex|2500|1.0|BTC|sell|",     # DEX sell 1.0 BTC for $2500
        "|cex|100|10.0|SOL|buy|",      # CEX buy 10.0 SOL for $100
        "|dex|0.5|1000.0|ADA|sell|",   # DEX sell 1000.0 ADA for $0.5
    ]
    
    print("\n📨 Processing CexTransaction events...")
    
    for i, event_data in enumerate(example_events, 1):
        print(f"\n--- Event {i} ---")
        print(f"Raw data: {event_data}")
        
        # Handle the CexTransaction event
        await business_service.handle_cex_transaction_event(event_data)
        
        # Small delay between events
        await asyncio.sleep(1)
    
    print("\n✅ Example completed!")
    print("\n🔧 Integration Notes:")
    print("- Replace demo credentials with real API keys")
    print("- Implement contract event listeners in start() method")
    print("- Add business logic in **PUT OPERATIONS BUSINESS HERE** sections")
    print("- Implement Odos integration in **PUT ODOS OPERATIONS HERE** sections")

if __name__ == "__main__":
    asyncio.run(main())
