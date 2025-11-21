from fastapi import APIRouter
from pipeline.quantum_pipeline_v7 import generate_daily_tips
from scraper.odds_scraper import collect_events

router = APIRouter()

@router.get("/daily")
def daily_tips():
    events = collect_events()
    return generate_daily_tips(events)

@router.get("/live")
def live_tips():
    events = collect_events()
    return [e for e in events if e.get("live")]
