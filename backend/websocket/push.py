from fastapi import APIRouter, WebSocket
from typing import List

router = APIRouter()
connections: List[WebSocket] = []


async def broadcast(message: dict):
    """
    Minden csatlakozott WebSocket kliensnek kiküldi az üzenetet.
    """
    for ws in connections:
        try:
            await ws.send_json(message)
        except:
            pass


@router.websocket("/ws/push")
async def websocket_push(ws: WebSocket):
    await ws.accept()
    connections.append(ws)

    try:
        while True:
            await ws.receive_text()  # keep-alive
    except:
        pass
    finally:
        connections.remove(ws)
