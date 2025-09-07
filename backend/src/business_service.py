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
            from config.settings import ODOS_API_KEY, WALLET_ADDRESS, ODOS_CHAIN_ID
            
            print(f"🦄 Executing DEX buy: {transaction.quantity} {transaction.pair}")
            
            async with OdosClient(ODOS_API_KEY) as odos:
                # Get token addresses for the selected chain
                token_addresses = self._get_token_addresses(transaction.pair)
                
                # Get the target token address
                target_token = token_addresses.get("_target_address")
                usdt_address = token_addresses.get("USDT")
                
                if not target_token or not usdt_address:
                    print(f"❌ Missing token addresses: target={target_token}, usdt={usdt_address}")
                    return None
                
                # Calculate amount in wei (assuming 18 decimals for most tokens)
                amount_wei = int(transaction.quantity * 1e18)
                
                print(f"💰 Swapping {transaction.quantity} {transaction.pair} using USDT")
                print(f"�� Chain ID: {ODOS_CHAIN_ID}")
                print(f"📍 Wallet: {WALLET_ADDRESS}")
                print(f"🪙 Target Token: {target_token}")
                print(f"💵 USDT Address: {usdt_address}")
                
                # Get quote from Odos
                quote = await odos.get_quote(
                    token_in=usdt_address,  # Buying with USDT
                    token_out=target_token,  # Getting the target token
                    amount=str(amount_wei),
                    chain_id=ODOS_CHAIN_ID,
                    user_address=WALLET_ADDRESS
                )
                
                print(f"📊 Odos quote received successfully!")
                print(f"   Input: {quote.get('inValues', ['N/A'])[0]} USDT")
                print(f"   Output: {quote.get('outValues', ['N/A'])[0]} {transaction.pair}")
                print(f"   Gas estimate: {quote.get('gasEstimate', 'N/A')}")
                print(f"   Price impact: {quote.get('priceImpact', 'N/A')}%")
                
                # Assemble transaction
                tx_data = await odos.assemble_transaction(
                    path_id=quote["pathId"],
                    user_address=WALLET_ADDRESS,
                    simulate=True  # Simulate for safety
                )
                
                print(f"🔧 Transaction assembled successfully!")
                print(f"   To: {tx_data['transaction']['to']}")
                print(f"   Value: {tx_data['transaction']['value']} ETH")
                print(f"   Gas: {tx_data['transaction']['gas']}")
                
                # Here you would send the transaction to the blockchain
                # This requires a wallet with private key and web3 integration
                print("⚠️  Transaction ready for blockchain execution")
                print("📝 To execute: Sign and broadcast the transaction data")
                
                return tx_data
                
        except Exception as e:
            print(f"❌ DEX buy execution failed: {e}")
            return None
    async def _execute_dex_sell(self, transaction: CexTransaction):
        """
        Execute DEX sell transaction using Odos.
        
        Args:
            transaction (CexTransaction): Transaction data
        """
        try:
            from src.odos_client import OdosClient
            from config.settings import ODOS_API_KEY, WALLET_ADDRESS, ODOS_CHAIN_ID
            
            print(f"🦄 Executing DEX sell: {transaction.quantity} {transaction.pair}")
            
            async with OdosClient(ODOS_API_KEY) as odos:
                # Get token addresses for the selected chain
                token_addresses = self._get_token_addresses(transaction.pair)
                
                # Get the target token address
                target_token = token_addresses.get("_target_address")
                usdt_address = token_addresses.get("USDT")
                
                if not target_token or not usdt_address:
                    print(f"❌ Missing token addresses: target={target_token}, usdt={usdt_address}")
                    return None
                
                # Calculate amount in wei (assuming 18 decimals for most tokens)
                amount_wei = int(transaction.quantity * 1e18)
                
                print(f"💰 Swapping {transaction.quantity} {transaction.pair} to USDT")
                print(f"🔄 Chain ID: {ODOS_CHAIN_ID}")
                print(f"📍 Wallet: {WALLET_ADDRESS}")
                print(f"🪙 Target Token: {target_token}")
                print(f"💵 USDT Address: {usdt_address}")
                
                # Get quote from Odos
                quote = await odos.get_quote(
                    token_in=target_token,  # Selling the token
                    token_out=usdt_address,  # Getting USDT
                    amount=str(amount_wei),
                    chain_id=ODOS_CHAIN_ID,
                    user_address=WALLET_ADDRESS
                )
                
                print(f"📊 Odos quote received successfully!")
                print(f"   Input: {quote.get('inValues', ['N/A'])[0]} {transaction.pair}")
                print(f"   Output: {quote.get('outValues', ['N/A'])[0]} USDT")
                print(f"   Gas estimate: {quote.get('gasEstimate', 'N/A')}")
                print(f"   Price impact: {quote.get('priceImpact', 'N/A')}%")
                
                # Assemble transaction
                tx_data = await odos.assemble_transaction(
                    path_id=quote["pathId"],
                    user_address=WALLET_ADDRESS,
                    simulate=True  # Simulate for safety
                )
                
                print(f"🔧 Transaction assembled successfully!")
                print(f"   To: {tx_data['transaction']['to']}")
                print(f"   Value: {tx_data['transaction']['value']} ETH")
                print(f"   Gas: {tx_data['transaction']['gas']}")
                
                # Here you would send the transaction to the blockchain
                print("⚠️  Transaction ready for blockchain execution")
                print("📝 To execute: Sign and broadcast the transaction data")
                
                return tx_data
                
        except Exception as e:
            print(f"❌ DEX sell execution failed: {e}")
            return None
    # Legacy methods for backward compatibility
    async def handle_contract_event(self, event_data: Dict[str, Any]):
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
        """Get token addresses for trading pair based on configured chain."""
        from config.settings import ODOS_CHAIN_ID
        from src.odos_client import OdosClient
        
        # Get common tokens for the configured chain
        odos_client = OdosClient()
        token_map = odos_client.get_common_tokens(ODOS_CHAIN_ID)
        
        # Add USDT if not present (most chains have USDT)
        if "USDT" not in token_map:
            if ODOS_CHAIN_ID == 1:  # Ethereum
                token_map["USDT"] = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
            elif ODOS_CHAIN_ID == 137:  # Polygon
                token_map["USDT"] = "0xc2132D05D31c914a87C6611C10748AEb04B58e8F"
            elif ODOS_CHAIN_ID == 42161:  # Arbitrum
                token_map["USDT"] = "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9"
            elif ODOS_CHAIN_ID == 10:  # Optimism
                token_map["USDT"] = "0x94b008aA00579c1307B0EF2c499aD98a8ce58e58"
            elif ODOS_CHAIN_ID == 8453:  # Base
                token_map["USDT"] = "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913"
            else:
                # Fallback - you should add more chains as needed
                token_map["USDT"] = "0x0000000000000000000000000000000000000000"
        
        # Map common trading pairs to their token addresses
        # For Base chain, ETH maps to WETH
        if ODOS_CHAIN_ID == 8453:  # Base
            pair_mapping = {
                "ETH": "WETH",
                "BTC": "WBTC" if "WBTC" in token_map else "BTC", 
                "MATIC": "WMATIC" if "WMATIC" in token_map else "MATIC",
                "AVAX": "WAVAX" if "WAVAX" in token_map else "AVAX",
                "BNB": "WBNB" if "WBNB" in token_map else "BNB",
            }
        else:
            # For other chains, use the same mapping
            pair_mapping = {
                "ETH": "WETH" if "WETH" in token_map else "ETH",
                "BTC": "WBTC" if "WBTC" in token_map else "BTC", 
                "MATIC": "WMATIC" if "WMATIC" in token_map else "MATIC",
                "AVAX": "WAVAX" if "WAVAX" in token_map else "AVAX",
                "BNB": "WBNB" if "WBNB" in token_map else "BNB",
            }
        
        # Get the actual token symbol for the pair
        actual_symbol = pair_mapping.get(pair, pair)
        
        if actual_symbol not in token_map:
            print(f"⚠️  Token address for {pair} not found in mapping for chain {ODOS_CHAIN_ID}")
            print(f"📝 Available tokens: {list(token_map.keys())}")
            print(f"🔍 Looking for: {actual_symbol}")
            # Return a placeholder - this will cause the transaction to fail gracefully
            return {"USDT": token_map.get("USDT", "0x0000000000000000000000000000000000000000")}
        
        # Return the full token map with the specific pair highlighted
        result = token_map.copy()
        result["_target_token"] = actual_symbol
        result["_target_address"] = token_map[actual_symbol]
        
        return result
