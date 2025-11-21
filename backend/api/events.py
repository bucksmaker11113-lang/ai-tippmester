from fastapi import APIRouter
from scrapers.tippmixpro_scraper import scrape_tippmixpro

router = APIRouter(prefix="/api/events", tags=["events"])

@router.get("/")
def get_tippmixpro_events():
    events = scrape_tippmixpro()
    return {"count": len(events), "events": events}
