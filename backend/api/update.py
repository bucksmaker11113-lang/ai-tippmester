from fastapi import APIRouter
from scrapers.tippmixpro_scraper import TippmixProScraper
from scrapers.international_scraper import InternationalScraper
from scrapers.odds_aggregator import OddsAggregator
from engine.quantum_synth_engine import QuantumSynthEngine

router = APIRouter()

@router.post("/tippmixpro")
async def update_tippmixpro():
    data = await TippmixProScraper.scrape()
    return {"status": "updated", "events": len(data)}

@router.post("/international")
async def update_international():
    data = await InternationalScraper.scrape()
    return {"status": "updated", "events": len(data)}

@router.post("/aggregate")
async def aggregate():
    data = OddsAggregator.aggregate_all()
    return {"status": "aggregated", "events": len(data)}
