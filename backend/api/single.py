from fastapi import APIRouter
from engine.single_tip_engine import SingleTipEngine
from engine.quantum_synth_engine import QuantumSynthEngine

router = APIRouter()

@router.get("/tips")
async def get_single_tips():
    engine = SingleTipEngine()
    tips = engine.generate()
    return {"tips": tips}
