from fastapi import APIRouter
from engine.kombi_tip_engine import KombiTipEngine

router = APIRouter()

@router.get("/tips")
async def get_kombi_tips():
    engine = KombiTipEngine()
    tips = engine.generate()
    return {"kombi_tips": tips}
