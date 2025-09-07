import aiohttp
import asyncio
from typing import Dict, Any, Optional
import json

class OdosClient:
    """Client for Odos API integration."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.base_url = "https://api.odos.xyz"
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def get_quote(self, token_in: str, token_out: str, amount: str, 
                       chain_id: int = 1, user_address: str = None) -> Dict[str, Any]:
        """
        Get quote from Odos API using the correct endpoint and format.
        
        Args:
            token_in: Input token address
            token_out: Output token address  
            amount: Amount to swap (in wei)
            chain_id: Blockchain chain ID
            user_address: User wallet address
            
        Returns:
            Quote data from Odos
        """
        if not self.session:
            raise Exception("Session not initialized")
        
        # Use the correct endpoint from your example
        url = f"{self.base_url}/sor/quote/v2"
        headers = {
            "Content-Type": "application/json"
        }
        
        # Add API key to headers if provided
        if self.api_key:
            headers["API-Key"] = self.api_key
        
        data = {
            "chainId": chain_id,
            "inputTokens": [{"tokenAddress": token_in, "amount": amount}],
            "outputTokens": [{"tokenAddress": token_out, "proportion": 1}],
            "slippageLimitPercent": 1,  # 1% slippage as in your example
            "userAddr": user_address or "0x0000000000000000000000000000000000000000"
        }
        
        try:
            async with self.session.post(url, headers=headers, json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    return result
                else:
                    error_text = await response.text()
                    raise Exception(f"ODOS API error {response.status}: {error_text}")
        except Exception as e:
            raise Exception(f"Failed to get Odos quote: {e}")
    
    async def assemble_transaction(self, path_id: str, user_address: str, 
                                 simulate: bool = True) -> Dict[str, Any]:
        """
        Assemble transaction for Odos.
        
        Args:
            path_id: Path ID from quote
            user_address: User wallet address
            simulate: Whether to simulate the transaction
            
        Returns:
            Transaction data
        """
        if not self.session:
            raise Exception("Session not initialized")
        
        url = f"{self.base_url}/sor/assemble"
        headers = {
            "Content-Type": "application/json"
        }
        
        # Add API key to headers if provided
        if self.api_key:
            headers["API-Key"] = self.api_key
        
        data = {
            "userAddr": user_address,
            "pathId": path_id,
            "simulate": simulate
        }
        
        try:
            async with self.session.post(url, headers=headers, json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    return result
                else:
                    error_text = await response.text()
                    raise Exception(f"ODOS API error {response.status}: {error_text}")
        except Exception as e:
            raise Exception(f"Failed to assemble Odos transaction: {e}")
    
    def get_supported_chains(self) -> Dict[int, str]:
        """
        Get supported chain IDs and their names.
        Based on common DEX aggregator support.
        """
        return {
            1: "Ethereum Mainnet",
            137: "Polygon",
            42161: "Arbitrum",
            10: "Optimism", 
            8453: "Base",
            56: "BSC",
            43114: "Avalanche",
            250: "Fantom",
            100: "Gnosis",
        }
    
    def get_common_tokens(self, chain_id: int) -> Dict[str, str]:
        """
        Get common token addresses for a given chain.
        These are placeholder addresses - you should update with real ones.
        """
        if chain_id == 1:  # Ethereum Mainnet
            return {
                "WETH": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                "USDC": "0xA0b86a33E6441b8c4C8C0e4b8b8b8b8b8b8b8b8b",
                "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
                "DAI": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
            }
        elif chain_id == 137:  # Polygon
            return {
                "WMATIC": "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270",
                "USDC": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
                "USDT": "0xc2132D05D31c914a87C6611C10748AEb04B58e8F",
                "DAI": "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063",
            }
        elif chain_id == 42161:  # Arbitrum
            return {
                "WETH": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
                "USDC": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
                "USDT": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
                "ARB": "0x912CE59144191C1204E64559FE8253a0e49E6548",
            }
        elif chain_id == 10:  # Optimism
            return {
                "WETH": "0x4200000000000000000000000000000000000006",
                "USDC": "0x7F5c764cBc14f9669B88837ca1490cCa17c31607",
                "USDT": "0x94b008aA00579c1307B0EF2c499aD98a8ce58e58",
                "OP": "0x4200000000000000000000000000000000000042",
            }
        elif chain_id == 8453:  # Base
            return {
                "WETH": "0x4200000000000000000000000000000000000006",
                "USDC": "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",
                "USDT": "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",
                "DAI": "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",
            }
        else:
            return {}
