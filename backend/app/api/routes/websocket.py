from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import asyncio
import json
from datetime import datetime

from app.services.data_provider import get_data_provider

router = APIRouter()

active_connections: List[WebSocket] = []

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

manager = ConnectionManager()

@router.websocket("/realtime")
async def websocket_realtime(websocket: WebSocket):
    await manager.connect(websocket)
    
    try:
        while True:
            provider = get_data_provider()
            df = provider.generate_mock_data(50)
            
            data = df.to_dict('records')
            
            message = {
                "type": "market_update",
                "data": data,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            await manager.send_personal_message(json.dumps(message), websocket)
            
            await asyncio.sleep(5)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)


@router.websocket("/subscribe")
async def websocket_subscribe(websocket: WebSocket):
    await manager.connect(websocket)
    subscribed_symbols = []
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("action") == "subscribe":
                subscribed_symbols = message.get("symbols", [])
                await manager.send_personal_message(
                    json.dumps({
                        "type": "subscription_confirmed",
                        "symbols": subscribed_symbols
                    }),
                    websocket
                )
            
            elif message.get("action") == "unsubscribe":
                subscribed_symbols = []
                await manager.send_personal_message(
                    json.dumps({
                        "type": "unsubscription_confirmed"
                    }),
                    websocket
                )
            
            if subscribed_symbols:
                provider = get_data_provider()
                df = provider.generate_mock_data(100)
                filtered = df[df['symbol'].isin(subscribed_symbols)]
                
                update = {
                    "type": "symbol_update",
                    "data": filtered.to_dict('records'),
                    "timestamp": datetime.utcnow().isoformat()
                }
                
                await manager.send_personal_message(json.dumps(update), websocket)
            
            await asyncio.sleep(2)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)
