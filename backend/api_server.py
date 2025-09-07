"""
FastAPI server for trading system frontend integration.
"""
import asyncio
import json
import os
import sys
from datetime import datetime
from typing import Dict, Any, Optional, List
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.business_service import BusinessService, CexTransaction, TransactionSide, ExchangeType
from src.order_client import BinanceOrderClient
from src.odos_client import OdosClient
from src.config_loader import config

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Trading System API",
    description="API for cryptocurrency trading system with CEX and DEX support",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
business_service = None
websocket_connections = []

# Pydantic models
class OrderRequest(BaseModel):
    symbol: str
    quantity: float

class DEXQuoteRequest(BaseModel):
    tokenIn: str
    tokenOut: str
    amount: str
    chainId: int

class DEXAssembleRequest(BaseModel):
    pathId: str
    userAddress: str

class EventRequest(BaseModel):
    event_data: str

# Dependency for API key validation
async def verify_api_key(x_api_key: str = Header(None)):
    if not x_api_key or x_api_key != os.getenv('FRONTEND_API_KEY', 'demo_key'):
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

# Initialize business service on startup
@app.on_event("startup")
async def startup_event():
    global business_service
    try:
        api_key = config.get_api_key()
        api_secret = config.get_api_secret()
        use_testnet = config.use_testnet()
        
        business_service = BusinessService(api_key, api_secret, use_testnet)
        print("✅ Business service initialized")
    except Exception as e:
        print(f"❌ Failed to initialize business service: {e}")

# Health check endpoint
@app.get("/api/health")
async def health_check():
    return {
        "success": True,
        "data": {
            "status": "healthy",
            "timestamp": int(datetime.now().timestamp() * 1000),
            "services": {
                "binance": "connected" if business_service else "disconnected",
                "odos": "available",
                "contract_listener": "running" if business_service else "stopped"
            }
        }
    }

# System status endpoint
@app.get("/api/status")
async def get_system_status():
    return {
        "success": True,
        "data": {
            "trading_enabled": True,
            "testnet_mode": config.use_testnet(),
            "supported_chains": [1, 137, 42161, 10, 8453],
            "supported_tokens": {
                "8453": ["WETH", "USDC", "USDT", "DAI"],
                "1": ["WETH", "USDC", "USDT", "DAI"],
                "137": ["WMATIC", "USDC", "USDT", "DAI"]
            }
        }
    }

# Account endpoints
@app.get("/api/account/info")
async def get_account_info(api_key: str = Depends(verify_api_key)):
    try:
        if not business_service:
            raise HTTPException(status_code=503, detail="Business service not initialized")
        
        account_info = business_service.order_client.get_account_info()
        return {
            "success": True,
            "data": account_info
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/account/balance/{asset}")
async def get_balance(asset: str, api_key: str = Depends(verify_api_key)):
    try:
        if not business_service:
            raise HTTPException(status_code=503, detail="Business service not initialized")
        
        balance = business_service.order_client.get_balance(asset)
        return {
            "success": True,
            "data": {
                "asset": asset,
                "balance": balance
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Market data endpoints
@app.get("/api/market/symbol/{symbol}")
async def get_symbol_info(symbol: str, api_key: str = Depends(verify_api_key)):
    try:
        if not business_service:
            raise HTTPException(status_code=503, detail="Business service not initialized")
        
        symbol_info = business_service.order_client.get_symbol_info(symbol)
        return {
            "success": True,
            "data": symbol_info
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/orders/open")
async def get_open_orders(api_key: str = Depends(verify_api_key)):
    try:
        if not business_service:
            raise HTTPException(status_code=503, detail="Business service not initialized")
        
        orders = business_service.order_client.get_open_orders()
        return {
            "success": True,
            "data": orders
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Trading endpoints
@app.post("/api/orders/buy/market")
async def place_market_buy_order(order: OrderRequest, api_key: str = Depends(verify_api_key)):
    try:
        if not business_service:
            raise HTTPException(status_code=503, detail="Business service not initialized")
        
        response = await asyncio.to_thread(
            business_service.order_client.place_market_buy_order,
            symbol=order.symbol,
            quantity=order.quantity
        )
        return {
            "success": True,
            "data": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/orders/sell/market")
async def place_market_sell_order(order: OrderRequest, api_key: str = Depends(verify_api_key)):
    try:
        if not business_service:
            raise HTTPException(status_code=503, detail="Business service not initialized")
        
        response = await asyncio.to_thread(
            business_service.order_client.place_market_sell_order,
            symbol=order.symbol,
            quantity=order.quantity
        )
        return {
            "success": True,
            "data": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/orders/{order_id}")
async def cancel_order(order_id: int, symbol: str = "BTCUSDT", api_key: str = Depends(verify_api_key)):
    try:
        if not business_service:
            raise HTTPException(status_code=503, detail="Business service not initialized")
        
        response = await asyncio.to_thread(
            business_service.order_client.cancel_order,
            symbol=symbol,
            order_id=order_id
        )
        return {
            "success": True,
            "data": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# DEX endpoints
@app.post("/api/dex/quote")
async def get_dex_quote(quote_request: DEXQuoteRequest, api_key: str = Depends(verify_api_key)):
    try:
        async with OdosClient() as odos:
            quote = await odos.get_quote(
                token_in=quote_request.tokenIn,
                token_out=quote_request.tokenOut,
                amount=quote_request.amount,
                chain_id=quote_request.chainId,
                user_address="0x742d35Cc6634C0532925a3b8D0C0C4C2C2C2C2C2"  # Demo address
            )
            return {
                "success": True,
                "data": quote
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/dex/assemble")
async def assemble_dex_transaction(assemble_request: DEXAssembleRequest, api_key: str = Depends(verify_api_key)):
    try:
        async with OdosClient() as odos:
            tx_data = await odos.assemble_transaction(
                path_id=assemble_request.pathId,
                user_address=assemble_request.userAddress,
                simulate=True
            )
            return {
                "success": True,
                "data": tx_data
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Event handling endpoint
@app.post("/api/events/trigger")
async def trigger_event(event: EventRequest, api_key: str = Depends(verify_api_key)):
    try:
        if not business_service:
            raise HTTPException(status_code=503, detail="Business service not initialized")
        
        await business_service.handle_cex_transaction_event(event.event_data)
        return {
            "success": True,
            "data": {
                "message": "Event processed successfully",
                "event_data": event.event_data
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket_connections.append(websocket)
    
    try:
        while True:
            # Keep connection alive and send periodic updates
            await asyncio.sleep(30)
            
            # Send system status
            status = {
                "type": "status_update",
                "data": {
                    "timestamp": int(datetime.now().timestamp() * 1000),
                    "connections": len(websocket_connections)
                }
            }
            await websocket.send_text(json.dumps(status))
            
    except WebSocketDisconnect:
        websocket_connections.remove(websocket)

# Broadcast function for WebSocket
async def broadcast_message(message: dict):
    for connection in websocket_connections:
        try:
            await connection.send_text(json.dumps(message))
        except:
            websocket_connections.remove(connection)

if __name__ == "__main__":
    print("🚀 Starting Trading System API Server...")
    print("📡 WebSocket: ws://localhost:8000/ws")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🔑 API Key: demo_key (configure FRONTEND_API_KEY in .env)")
    
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
