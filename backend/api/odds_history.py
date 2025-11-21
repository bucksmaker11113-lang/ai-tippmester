from fastapi import APIRouter
from services.odds_history_service import fetch_event_history
from typing import List

router = APIRouter(prefix="/api/odds", tags=["odds_history"])


@router.get("/history/{event_name}")
def get_event_history(event_name: str):
    """
    Visszaadja egy esemény odds történetét.
    """
    return {
        "event": event_name,
        "history": fetch_event_history(event_name)
    }
