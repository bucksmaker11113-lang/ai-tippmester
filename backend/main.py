# ======================================================================
#  TIPPMESTER QUANTUM ENGINE – MAIN API CONTROLLER (v7.5 ULTRA FINAL)
# ======================================================================

import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers
from api.single import router as single_router
from api.kombi import router as kombi_router
from api.live import router as live_router
from api.update import router as update_router
from api.status import router as status_router
from api.health import router as health_router

# Scheduler
from scheduler.auto_update import auto_update_loop

# Quantum Engine Core
from engine.quantum_synth_engine import QuantumSynthEngine

# TippmixPro scraper initial
from scrapers.tippmixpro_scraper import TippmixProScraper


app = FastAPI(
    title="Tippmester Quantum Engine API",
    version="7.5 ULTRA",
    description="AI alapú sportfogadás · MonteCarlo v3 · GNN · LSTM · RL · Kelly · TippmixPro integráció"
)

# ======================================================================
#  CORS
# ======================================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================================================================
#  GLOBAL ENGINE INSTANCE
# ======================================================================
quantum_engine = QuantumSynthEngine()

# ======================================================================
#  STARTUP EVENT
# ======================================================================
@app.on_event("startup")
async def startup_event():

    print("\n[STARTUP] Tippmester Quantum Engine indul...\n")

    print("[STARTUP] Első TippmixPro scrape...")
    tippmix_data = await TippmixProScraper.scrape()
    quantum_engine.set_tippmix_data(tippmix_data)

    print("[STARTUP] TippmixPro adat betöltve.")

    print("[STARTUP] Automata workflow indítása (5 percenként)...")
    asyncio.create_task(auto_update_loop(quantum_engine))

    print("[STARTUP] Rendszer készen áll.\n")

# ======================================================================
#  ROUTERS
# ======================================================================
app.include_router(single_router, prefix="/single", tags=["Single Tips"])
app.include_router(kombi_router, prefix="/kombi", tags=["Kombi Tips"])
app.include_router(live_router, prefix="/live", tags=["Live Tips"])
app.include_router(update_router, prefix="/update", tags=["Scraper"])
app.include_router(status_router, prefix="/status", tags=["Status"])
app.include_router(health_router, prefix="/health", tags=["Health"])


# ======================================================================
#  ROOT
# ======================================================================
@app.get("/")
async def root():
    return {
        "engine": "Tippmester Quantum Engine 7.5 ULTRA",
        "status": "running",
        "message": "API OK"
    }


# ======================================================================
#  DEV ENTRY POINT
# ======================================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
