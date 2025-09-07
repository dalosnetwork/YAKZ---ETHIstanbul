import asyncio
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import sys
import os

# Add the parent directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.order_client import BinanceOrderClient

class TransactionSide(Enum):
    """Transaction side enumeration."""
    BUY = "buy"
    SELL = "sell"

class ExchangeType(Enum):
    """Exchange type enumeration."""
    CEX = "cex"
    DEX = "dex"

@dataclass
class CexTransaction:
    """CexTransaction event data structure."""
    ex_type: ExchangeType
    quantity: float
    expected_price: float
    pair: str
    transaction_side: TransactionSide
    
    @classmethod
    def from_event_data(cls, event_data: str) -> 'CexTransaction':
        """
        Parse CexTransaction from event data string.
        
        Args:
            event_data (str): Event data in format "|ex_type|quantity|expected_price|pair|transaction_side|"
            
        Returns:
            CexTransaction: Parsed transaction data
        """
        # Remove leading/trailing pipes and split
        parts = event_data.strip('|').split('|')
        
        if len(parts) != 5:
            raise ValueError(f"Invalid event data format. Expected 5 parts, got {len(parts)}")
        
        ex_type_str, quantity_str, price_str, pair_str, side_str = parts
        
        return cls(
            ex_type=ExchangeType(ex_type_str.lower()),
            quantity=float(quantity_str),
            expected_price=float(price_str),
            pair=pair_str.upper(),
            transaction_side=TransactionSide(side_str.lower())
        )

class BusinessService:
    """
    Business service that handles CexTransaction events and executes trades.
    This service runs alongside the main application.
    """
    
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        """
        Initialize the business service.
        
        Args:
            api_key (str): Binance API key
            api_secret (str): Binance API secret
            testnet (bool): Whether to use testnet
        """
        self.order_client = BinanceOrderClient(api_key, api_secret, testnet)
        self.running = False
        print(f"🏢 Business Service initialized ({'TESTNET' if testnet else 'MAINNET'})")
    
    async def start(self):
        """Start the business service."""
        self.running = True
        print("🚀 Business Service started")
        
        while self.running:
            try:
                # **PUT OPERATIONS BUSINESS HERE**
                # Your friend will implement:
                # - Contract event listeners
                # - Event polling/websocket connections
                # - Background monitoring tasks
                
                # Keep the service running
                await asyncio.sleep(1)
                
            except Exception as e:
                print(f"❌ Business Service error: {e}")
                await asyncio.sleep(5)
    
    def stop(self):
        """Stop the business service."""
        self.running = False
        print("🛑 Business Service stopped")
    
    async def handle_cex_transaction_event(self, event_data: str):
        """
        Handle incoming CexTransaction events.
        
        Args:
            event_data (str): Event data in format "|ex_type|quantity|expected_price|pair|transaction_side|"
        """
        try:
            # Parse the event data
            transaction = CexTransaction.from_event_data(event_data)
            
            print(f"📨 CexTransaction event received:")
            print(f"   Exchange: {transaction.ex_type.value}")
            print(f"   Pair: {transaction.pair}")
            print(f"   Side: {transaction.transaction_side.value}")
            print(f"   Quantity: {transaction.quantity}")
            print(f"   Expected Price: ${transaction.expected_price}")
            
            # **PUT OPERATIONS BUSINESS HERE**
            # Your friend will implement:
            # - Risk management checks
            # - Position sizing logic
            # - Market condition analysis
            # - Custom business rules
            
            # Risk management checks
            if not await self._perform_risk_checks(transaction):
                print("❌ Transaction blocked by risk management")
                return
            
            # Position sizing logic
            adjusted_transaction = await self._adjust_position_size(transaction)
            
            # Market condition analysis
            if not await self._check_market_conditions(adjusted_transaction):
                print("❌ Transaction blocked by market conditions")
                return
            
            # Execute based on exchange type
            if adjusted_transaction.ex_type == ExchangeType.CEX:
                await self._execute_cex_transaction(adjusted_transaction)
            elif adjusted_transaction.ex_type == ExchangeType.DEX:
                await self._execute_dex_transaction(adjusted_transaction)
            else:
                print(f"❌ Unknown exchange type: {adjusted_transaction.ex_type}")
                
        except Exception as e:
            print(f"❌ Error handling CexTransaction event: {e}")
    
    async def _perform_risk_checks(self, transaction: CexTransaction) -> bool:
        """Perform risk management checks."""
        try:
            # Check minimum trade size
            if transaction.quantity < 0.001:
                print("❌ Transaction quantity too small")
                return False
            
            # Check maximum trade size (adjust as needed)
            max_trade_size = 10000  # USDT
            trade_value = transaction.quantity * transaction.expected_price
            if trade_value > max_trade_size:
                print("❌ Transaction size exceeds maximum limit")
                return False
            
            # Check account balance
            required_balance = trade_value if transaction.transaction_side == TransactionSide.BUY else transaction.quantity
            asset = "USDT" if transaction.transaction_side == TransactionSide.BUY else transaction.pair
            
            try:
                balance = self.order_client.get_balance(asset)
                if balance < required_balance:
                    print(f"❌ Insufficient balance: {balance} {asset} < {required_balance}")
                    return False
            except Exception as e:
                print(f"⚠️  Could not check balance: {e}")
            
            return True
            
        except Exception as e:
            print(f"❌ Risk check error: {e}")
            return False
    
    async def _adjust_position_size(self, transaction: CexTransaction) -> CexTransaction:
        """Adjust position size based on current holdings and risk."""
        try:
            # Check current position size
            current_balance = self.order_client.get_balance(transaction.pair)
            
            # Calculate position size adjustment
            max_position_ratio = 0.1  # Maximum 10% of portfolio per asset
            portfolio_value = self.order_client.get_balance("USDT") + (current_balance * transaction.expected_price)
            max_position_value = portfolio_value * max_position_ratio
            
            trade_value = transaction.quantity * transaction.expected_price
            
            if trade_value > max_position_value:
                # Adjust quantity to respect position limits
                adjusted_quantity = max_position_value / transaction.expected_price
                transaction.quantity = adjusted_quantity
                print(f"⚠️  Adjusted position size to {adjusted_quantity} due to risk limits")
            
            return transaction
            
        except Exception as e:
            print(f"⚠️  Position sizing error: {e}")
            return transaction
    
    async def _check_market_conditions(self, transaction: CexTransaction) -> bool:
        """Check current market conditions."""
        try:
            # Add your market analysis logic here
            # For example: volatility checks, spread analysis, etc.
            
            # Placeholder: simple check
            if transaction.expected_price <= 0:
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Market condition check error: {e}")
            return False
    
    async def _execute_cex_transaction(self, transaction: CexTransaction):
        """
        Execute CEX transaction using Binance API.
        
        Args:
            transaction (CexTransaction): Transaction data
        """
        print(f"🏦 Executing CEX transaction: {transaction.transaction_side.value} {transaction.quantity} {transaction.pair}")
        
        # **PUT OPERATIONS BUSINESS HERE**
        # Your friend will implement:
        # - Pre-execution validation
        # - Risk checks
        # - Position sizing
        # - Price validation
        
        try:
            if transaction.transaction_side == TransactionSide.BUY:
                # Calculate USDT amount to spend
                usdt_amount = transaction.quantity * transaction.expected_price
                
                # **PUT OPERATIONS BUSINESS HERE**
                # Your friend will implement buy order logic:
                # - Market vs limit order decision
                # - Slippage protection
                # - Order size validation
                
                response = self.order_client.place_market_buy_order(
                    symbol=f"{transaction.pair}USDT",
                    quote_order_qty=usdt_amount
                )
                print(f"✅ CEX Buy order executed: {response}")
                
            elif transaction.transaction_side == TransactionSide.SELL:
                # **PUT OPERATIONS BUSINESS HERE**
                # Your friend will implement sell order logic:
                # - Balance validation
                # - Market vs limit order decision
                # - Order size validation
                
                response = self.order_client.place_market_sell_order(
                    symbol=f"{transaction.pair}USDT",
                    quantity=transaction.quantity
                )
                print(f"✅ CEX Sell order executed: {response}")
                
        except Exception as e:
            print(f"❌ CEX transaction failed: {e}")
    
    async def _execute_dex_transaction(self, transaction: CexTransaction):
        """
        Execute DEX transaction using Odos integration.
        
        Args:
            transaction (CexTransaction): Transaction data
        """
        print(f"🦄 Executing DEX transaction: {transaction.transaction_side.value} {transaction.quantity} {transaction.pair}")
        
        # **PUT OPERATIONS BUSINESS HERE**
        # Your friend will implement:
        # - Pre-execution validation
        # - DEX-specific risk checks
        # - Gas fee estimation
        # - Slippage protection
        
        try:
            if transaction.transaction_side == TransactionSide.BUY:
                await self._execute_dex_buy(transaction)
            elif transaction.transaction_side == TransactionSide.SELL:
                await self._execute_dex_sell(transaction)
                
        except Exception as e:
            print(f"❌ DEX transaction failed: {e}")
    
    async def _execute_dex_buy(self, transaction: CexTransaction):
        """
        Execute DEX buy transaction using Odos.
        
        Args:
            transaction (CexTransaction): Transaction data
        """
        try:
            from src.odos_client import OdosClient
            
            async with OdosClient("YOUR_ODOS_API_KEY") as odos:
                # Get token addresses (you'll need to maintain a mapping)
                token_addresses = self._get_token_addresses(transaction.pair)
                
                # Calculate amount in wei
                amount_wei = int(transaction.quantity * 1e18)  # Assuming 18 decimals
                
                # Get quote from Odos
                quote = await odos.get_quote(
                    token_in=token_addresses["USDT"],
                    token_out=token_addresses[transaction.pair],
                    amount=str(amount_wei)
                )
                
                print(f"📊 Odos quote received: {quote}")
                
                # Assemble transaction
                tx_data = await odos.assemble_transaction(
                    path_id=quote["pathId"],
                    user_address="YOUR_WALLET_ADDRESS"  # Replace with actual address
                )
                
                print(f"🦄 DEX Buy transaction assembled: {tx_data}")
                
                # Here you would send the transaction to the blockchain
                # This requires a wallet with private key
                # await self._send_blockchain_transaction(tx_data)
                
        except Exception as e:
            print(f"❌ DEX buy execution failed: {e}")
    
    async def _execute_dex_sell(self, transaction: CexTransaction):
        """
        Execute DEX sell transaction using Odos.
        
        Args:
            transaction (CexTransaction): Transaction data
        """
        try:
            from src.odos_client import OdosClient
            
            async with OdosClient("YOUR_ODOS_API_KEY") as odos:
                # Get token addresses
                token_addresses = self._get_token_addresses(transaction.pair)
                
                # Calculate amount in wei
                amount_wei = int(transaction.quantity * 1e18)
                
                # Get quote from Odos
                quote = await odos.get_quote(
                    token_in=token_addresses[transaction.pair],
                    token_out=token_addresses["USDT"],
                    amount=str(amount_wei)
                )
                
                print(f"📊 Odos quote received: {quote}")
                
                # Assemble transaction
                tx_data = await odos.assemble_transaction(
                    path_id=quote["pathId"],
                    user_address="YOUR_WALLET_ADDRESS"
                )
                
                print(f"🦄 DEX Sell transaction assembled: {tx_data}")
                
                # Here you would send the transaction to the blockchain
                # await self._send_blockchain_transaction(tx_data)
                
        except Exception as e:
            print(f"❌ DEX sell execution failed: {e}")    async def handle_contract_event(self, event_data: Dict[str, Any]):
        """
        Legacy method for handling contract events.
        Redirects to new CexTransaction handler.
        
        Args:
            event_data (dict): Contract event data
        """
        # **PUT OPERATIONS BUSINESS HERE**
        # Your friend can implement custom event handling here
        # or convert to CexTransaction format
        
        print(f"📨 Legacy contract event received: {event_data}")
    
    async def execute_buy_order(self, symbol: str, amount: float):
        """
        Legacy method for executing buy orders.
        
        Args:
            symbol (str): Trading symbol
            amount (float): USDT amount to spend
        """
        # **PUT OPERATIONS BUSINESS HERE**
        
        try:
            response = self.order_client.place_market_buy_order(
                symbol=symbol,
                quote_order_qty=amount
            )
            print(f"✅ Buy order executed: {response}")
        except Exception as e:
            print(f"❌ Buy order failed: {e}")
    
    async def execute_sell_order(self, symbol: str, quantity: float):
        """
        Legacy method for executing sell orders.
        
        Args:
            symbol (str): Trading symbol
            quantity (float): Quantity to sell
        """
        # **PUT OPERATIONS BUSINESS HERE**
        
        try:
            response = self.order_client.place_market_sell_order(
                symbol=symbol,
                quantity=quantity
            )
            print(f"✅ Sell order executed: {response}")
        except Exception as e:
            print(f"❌ Sell order failed: {e}")

    async def _perform_risk_checks(self, transaction: CexTransaction) -> bool:
        """Perform risk management checks."""
        try:
            # Check minimum trade size
            if transaction.quantity < 0.001:
                print("❌ Transaction quantity too small")
                return False
            
            # Check maximum trade size (adjust as needed)
            max_trade_size = 10000  # USDT
            trade_value = transaction.quantity * transaction.expected_price
            if trade_value > max_trade_size:
                print("❌ Transaction size exceeds maximum limit")
                return False
            
            # Check account balance
            required_balance = trade_value if transaction.transaction_side == TransactionSide.BUY else transaction.quantity
            asset = "USDT" if transaction.transaction_side == TransactionSide.BUY else transaction.pair
            
            try:
                balance = self.order_client.get_balance(asset)
                if balance < required_balance:
                    print(f"❌ Insufficient balance: {balance} {asset} < {required_balance}")
                    return False
            except Exception as e:
                print(f"⚠️  Could not check balance: {e}")
            
            return True
            
        except Exception as e:
            print(f"❌ Risk check error: {e}")
            return False
    
    async def _adjust_position_size(self, transaction: CexTransaction) -> CexTransaction:
        """Adjust position size based on current holdings and risk."""
        try:
            # Check current position size
            current_balance = self.order_client.get_balance(transaction.pair)
            
            # Calculate position size adjustment
            max_position_ratio = 0.1  # Maximum 10% of portfolio per asset
            portfolio_value = self.order_client.get_balance("USDT") + (current_balance * transaction.expected_price)
            max_position_value = portfolio_value * max_position_ratio
            
            trade_value = transaction.quantity * transaction.expected_price
            
            if trade_value > max_position_value:
                # Adjust quantity to respect position limits
                adjusted_quantity = max_position_value / transaction.expected_price
                transaction.quantity = adjusted_quantity
                print(f"⚠️  Adjusted position size to {adjusted_quantity} due to risk limits")
            
            return transaction
            
        except Exception as e:
            print(f"⚠️  Position sizing error: {e}")
            return transaction
    
    async def _check_market_conditions(self, transaction: CexTransaction) -> bool:
        """Check current market conditions."""
        try:
            # Add your market analysis logic here
            # For example: volatility checks, spread analysis, etc.
            
            # Placeholder: simple check
            if transaction.expected_price <= 0:
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Market condition check error: {e}")
            return False
    
    async def _handle_contract_event(self, event_data):
        """Handle incoming contract events."""
        try:
            args = event_data['args']
            
            # Convert contract event to CexTransaction format
            event_string = f"|{args['exType']}|{args['quantity']/1e18}|{args['expectedPrice']/1e18}|{args['pair']}|{args['side']}|"
            
            # Process the event
            await self.handle_cex_transaction_event(event_string)
            
        except Exception as e:
            print(f"❌ Error handling contract event: {e}")

    def _get_token_addresses(self, pair: str) -> Dict[str, str]:
        """Get token addresses for trading pair."""
        # You should maintain a mapping of token symbols to addresses
        token_map = {
            "ETH": "0x0000000000000000000000000000000000000000",  # Replace with actual addresses
            "BTC": "0x0000000000000000000000000000000000000000",
            "USDT": "0x0000000000000000000000000000000000000000",
            # Add more tokens as needed
        }
        return token_map
