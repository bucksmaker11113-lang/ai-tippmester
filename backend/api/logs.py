from fastapi import APIRouter
from database.db import SessionLocal
from database.models import TipSingle, TipKombi, TipLive, BankrollLog, OddsHistory, LiveStatsHistory

router = APIRouter(prefix="/api/logs", tags=["logs"])

db = SessionLocal()

@router.get("/single")
def get_single_logs():
    return db.query(TipSingle).all()

@router.get("/kombi")
def get_kombi_logs():
    return db.query(TipKombi).all()

@router.get("/live")
def get_live_logs():
    return db.query(TipLive).all()

@router.get("/bankroll")
def get_bankroll_logs():
    return db.query(BankrollLog).all()

@router.get("/odds")
def get_odds_history():
    return db.query(OddsHistory).all()

@router.get("/live_stats")
def get_live_stats_history():
    return db.query(LiveStatsHistory).all()
