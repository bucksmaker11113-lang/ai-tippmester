from fastapi import APIRouter, WebSocket

router = APIRouter()

@router.websocket("/ws/live")
async def websocket_live(ws: WebSocket):
    await ws.accept()
    while True:
        await ws.send_text("live-ping")  # később élő tipp stream jön ide
