# ============================================================
# realtime.py — WebSocket for Live Price Streaming (Simulated)
# ============================================================

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio, random

router = APIRouter()

clients = []

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Simulates real-time stock updates.
    You can later replace this with live NSE/BSE feed logic.
    """
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = {
                "ticker": random.choice(["INFY", "TCS", "HDFC", "SBIN", "RELIANCE"]),
                "price": round(random.uniform(900, 3500), 2)
            }
            for ws in clients:
                await ws.send_json(data)
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        clients.remove(websocket)
