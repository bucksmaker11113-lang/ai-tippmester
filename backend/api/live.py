from fastapi import APIRouter
from engine.live_engine import choose_live_tips

router = APIRouter(prefix="/api/live", tags=["live"])

@router.get("/")
def get_live_tips():
    live_feed = []   # később → live odds input
    tips = choose_live_tips(live_feed)
    return {"count": len(tips), "tips": tips}
