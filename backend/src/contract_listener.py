import asyncio
import json
from web3 import Web3
from typing import Dict, Any, Callable, Optional
import logging

class SmartContractListener:
    """
    Smart contract event listener for processing trading signals.
    Listens to specific contract events and triggers trading operations.
    """
    
    def __init__(self, rpc_url: str, contract_address: str, abi: list, 
                 event_handler: Callable[[Dict[str, Any]], None]):
        """
        Initialize the contract listener.
        
        Args:
            rpc_url (str): Ethereum RPC URL
            contract_address (str): Contract address to monitor
            abi (list): Contract ABI
            event_handler (Callable): Function to handle events
        """
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.contract_address = contract_address
        self.contract_abi = abi
        self.event_handler = event_handler
        self.running = False
        
        # Create contract instance
        self.contract = self.w3.eth.contract(
            address=contract_address,
            abi=abi
        )
        
        print(f"📡 Contract Listener initialized for {contract_address}")
    
    async def start_listening(self):
        """Start listening to contract events."""
        self.running = True
        print("🚀 Contract event listener started")
        
        # Create event filter for specific events
        event_filter = self.contract.events.TradingSignal.createFilter(
            fromBlock='latest'
        )
        
        while self.running:
            try:
                # Get new events
                entries = event_filter.get_new_entries()
                
                for event in entries:
                    await self._process_event(event)
                
                # Wait before checking again
                await asyncio.sleep(2)
                
            except Exception as e:
                print(f"❌ Contract listener error: {e}")
                await asyncio.sleep(5)
    
    async def _process_event(self, event):
        """Process individual contract event."""
        try:
            # Extract event data
            event_data = {
                'address': event['address'],
                'blockNumber': event['blockNumber'],
                'transactionHash': event['transactionHash'].hex(),
                'args': dict(event['args'])
            }
            
            print(f"📨 Contract event received: {event_data['transactionHash']}")
            
            # Call the event handler
            if self.event_handler:
                await self.event_handler(event_data)
                
        except Exception as e:
            print(f"❌ Error processing contract event: {e}")
    
    def stop(self):
        """Stop the contract listener."""
        self.running = False
        print("🛑 Contract listener stopped")
