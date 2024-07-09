import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core import socket_manager

router = APIRouter(
    prefix="/ws",
    tags=["websocket"],
)


@router.websocket("/test/{client_id}/")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await socket_manager.connect(websocket)
    try:
        while True:
            receive_task = asyncio.create_task(websocket.receive_text())
            done, pending = await asyncio.wait(
                [receive_task],
                return_when=asyncio.FIRST_COMPLETED,
            )
            if receive_task in done:
                data = receive_task.result()
                await socket_manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        socket_manager.disconnect(websocket)
        await socket_manager.broadcast(f"Client #{client_id} disconnected")


@router.get('/salom/')
async def salom_endpoint():
    return {'salom': "salom"}
