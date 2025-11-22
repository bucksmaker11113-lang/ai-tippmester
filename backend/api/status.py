from fastapi import APIRouter
from engine.quantum_synth_engine import QuantumSynthEngine

router = APIRouter()

@router.get("/")
async def status():
    return {
        "quantum_engine": "ready",
        "version": "7.5 ULTRA",
        "message": "System running"
    }
