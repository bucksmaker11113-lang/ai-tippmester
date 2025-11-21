from fastapi import APIRouter
from engine.single_engine import choose_best_single_per_sport
from engine.value_scanner import scan_value_events

router = APIRouter(prefix="/api/single", tags=["single"])

@router.get("/")
def get_single_tips():
    # Itt majd az odds feed → value events kerül betöltésre
    # most placeholder input
    events = []  # később scraper + mapper
    value_events = scan_value_events(events)
    singles = choose_best_single_per_sport(value_events)
    return {"count": len(singles), "tips": singles}
