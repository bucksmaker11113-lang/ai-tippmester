from database.db import SessionLocal
from database.models import OddsHistory
from datetime import datetime

db = SessionLocal()

def record_odds(event_name: str, bookmaker: str, odds: float):
    """
    Odds-történet naplózása minden változáskor.
    """
    obj = OddsHistory(
        event=event_name,
        book=bookmaker,
        odds=odds,
        timestamp=datetime.utcnow()
    )
    db.add(obj)
    db.commit()


def fetch_event_history(event_name: str):
    """
    Adott esemény teljes odds története időrendben.
    """
    result = db.query(OddsHistory).filter(
        OddsHistory.event == event_name
    ).order_by(OddsHistory.timestamp.asc()).all()

    return [
        {
            "timestamp": item.timestamp.isoformat(),
            "book": item.book,
            "odds": item.odds
        }
        for item in result
    ]
