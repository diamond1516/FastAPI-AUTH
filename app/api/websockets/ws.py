from fastapi import APIRouter, WebSocket, Depends, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from app.core.websocket_manager import socket_manager

router = APIRouter(
    prefix="/ws",
    tags=["websockets"],
)


@router.websocket("/test/{client_id}/")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await socket_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await socket_manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        socket_manager.disconnect(websocket)
        await socket_manager.broadcast(f"Client #{client_id} disconnected")


@router.get('/salom/')
async def salom_endpoint():
    return {'salom': "salom"}
