from fastapi import APIRouter
from engine.live_tip_engine import LiveTipEngine

router = APIRouter()

@router.get("/now")
async def get_live_tip():
    engine = LiveTipEngine()
    tip = engine.generate()
    return {"live_tip": tip}
