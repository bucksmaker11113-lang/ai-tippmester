# ==============================================================================
#                 TIPPMESTER QUANTUM ENGINE – MAIN API 7.5 ULTRA
# ------------------------------------------------------------------------------
#   FUNKCIÓK:
#       ✓ TippmixPro scraper automata frissítés
#       ✓ Single tippek API
#       ✓ Kombi tippek API
#       ✓ Élő tippek API
#       ✓ Scheduler automata workflow (5 percenként update)
#       ✓ Költséghatékony mód (low-resource operations)
# ==============================================================================

from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
import uvicorn
import time

from engine.quantum_synth_engine import quantum_synth
from engine.tippmixpro_engine import tippmix_engine
from scraper.tippmix_scraper import tippmixpro_scraper


# ------------------------------------------------------------------------------
# MODELS
# ------------------------------------------------------------------------------

class Event(BaseModel):
    sport: str
    match: str
    odds: float
    team_graph: dict = {}
    stats: dict = {}
    odds_history: list = []
    market_volume: float = 0.0
    market_volatility: float = 0.0


class LiveEvent(BaseModel):
    match: str
    odds: float
    live_stats: dict


class EventsRequest(BaseModel):
    events: list[Event]


# ------------------------------------------------------------------------------
# FASTAPI APP
# ------------------------------------------------------------------------------

app = FastAPI(
    title="Tippmester Quantum Engine API 7.5 ULTRA",
    version="7.5",
    description="AI alapú sportfogadási rendszer – MonteCarlo + GNN + LSTM + Kelly + TippmixPro integráció"
)


# ------------------------------------------------------------------------------
# ENDPOINT: TippmixPro Scraper Manual Trigger
# ------------------------------------------------------------------------------

@app.get("/update_tippmix")
async def update_tippmix():
    print("[API] TippmixPro scraping started…")
    data = await tippmixpro_scraper.scrape()
    tippmix_engine.set_data(data)
    return {"status": "updated", "items": len(data)}


# ------------------------------------------------------------------------------
# ENDPOINT: Single Tips
# ------------------------------------------------------------------------------

@app.post("/single_tips")
async def single_tips(input: EventsRequest):
    events = [e.dict() for e in input.events]
    tips = quantum_synth.generate_single_tips(events)
    return {"single_tips": tips}


# ------------------------------------------------------------------------------
# ENDPOINT: Kombi Tips
# ------------------------------------------------------------------------------

@app.post("/kombi_tip")
async def kombi_tip(input: EventsRequest):
    events = [e.dict() for e in input.events]
    tips = quantum_synth.generate_kombi_tip(events)
    return {"kombi_tip": tips}


# ------------------------------------------------------------------------------
# ENDPOINT: Live Tip
# ------------------------------------------------------------------------------

@app.post("/live_tip")
async def live_tip(input: LiveEvent):
    tip = quantum_synth.generate_live_tip(
        live_stats=input.live_stats,
        odds=input.odds
    )
    return {"live_tip": tip}


# ------------------------------------------------------------------------------
# ENGINE STATUS
# ------------------------------------------------------------------------------

@app.get("/status")
async def status():
    return {
        "engine": "QuantumSynth 7.5 ULTRA",
        "tippmix_items": len(tippmix_engine.tippmix_data),
        "scheduler": scheduler_running
    }


# ------------------------------------------------------------------------------
# AUTOMATA WORKFLOW – 5 percenként frissít
# ------------------------------------------------------------------------------

scheduler_running = False

async def auto_workflow():
    global scheduler_running
    scheduler_running = True

    while True:
        print("\n[AUTO] TippmixPro automata frissítés...")
        data = await tippmixpro_scraper.scrape()
        tippmix_engine.set_data(data)

        print("[AUTO] Készen. Következő ciklus: 5 perc múlva.\n")
        await asyncio.sleep(300)   # 5 perc


# ------------------------------------------------------------------------------
# STARTUP EVENT – scheduler indítása
# ------------------------------------------------------------------------------

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(auto_workflow())


# ------------------------------------------------------------------------------
# ENTRY POINT
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
