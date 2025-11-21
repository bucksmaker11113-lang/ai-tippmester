from fastapi import APIRouter
from scrapers.international_live_scraper import scrape_international_live

router = APIRouter(prefix="/api/international/live", tags=["international_live"])


@router.get("/")
def get_international_live():
    """
    Élő OddsPortal feed:
    - current_odds
    - prev_odds → odds drop
    - momentum input
    """
    data = scrape_international_live()
    return {
        "count": len(data),
        "events": data
    }
