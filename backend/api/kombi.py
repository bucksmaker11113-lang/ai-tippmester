from fastapi import APIRouter
from engine.kombi_engine import choose_kombi_tips
from engine.single_engine import choose_best_single_per_sport
from engine.value_scanner import scan_value_events

router = APIRouter(prefix="/api/kombi", tags=["kombi"])

@router.get("/")
def get_kombi_tips():
    events = []
    value_events = scan_value_events(events)
    singles = choose_best_single_per_sport(value_events)
    kombi = choose_kombi_tips(value_events, singles)
    return {"count": len(kombi), "tips": kombi}
