from fastapi import APIRouter
from scrapers.international_odds_scraper import scrape_international_all

router = APIRouter(prefix="/api/international", tags=["international"])


@router.get("/")
def get_international_odds():
    """
    OddsPortal sportágankénti odds aggregator:
    - foci
    - kosár
    - hoki
    - tenisz
    """
    data = scrape_international_all()
    return {
        "count": len(data),
        "events": data
    }
