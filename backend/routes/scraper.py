from fastapi import APIRouter
from scraper.odds_scraper import collect_events

router = APIRouter()

@router.get("/events")
def get_events():
    return collect_events()
