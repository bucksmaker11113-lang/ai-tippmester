from fastapi import APIRouter
from scrapers.sofascore_live_scraper import scrape_sofascore_live

router = APIRouter(prefix="/api/sofa/live", tags=["sofa_live"])

@router.get("/")
def get_sofa_live():
    data = scrape_sofascore_live()
    return {"count": len(data), "events": data}
