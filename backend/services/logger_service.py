from database.db import SessionLocal
from database.models import TipSingle, TipKombi, TipLive, BankrollLog, OddsHistory, LiveStatsHistory


db = SessionLocal()

# ----------------------------
# TIPPEK MENTÉSE
# ----------------------------

def log_single_tip(t):
    obj = TipSingle(
        sport=t["sport"],
        team1=t["team1"],
        team2=t["team2"],
        odds=t.get("tippmix_odds", 0),
        strength=t.get("strength", 0)
    )
    db.add(obj)
    db.commit()


def log_kombi_tip(events, total_odds, strength):
    obj = TipKombi(
        events=events,
        total_odds=total_odds,
        strength=strength
    )
    db.add(obj)
    db.commit()


def log_live_tip(t):
    obj = TipLive(
        team1=t["team1"],
        team2=t["team2"],
        odds=t["current_odds"],
        momentum=t["momentum"],
        live_strength=t["live_strength"]
    )
    db.add(obj)
    db.commit()


# ----------------------------
# BANKROLL LOG
# ----------------------------

def log_bankroll(category, amount, balance):
    obj = BankrollLog(
        category=category,
        amount=amount,
        balance=balance
    )
    db.add(obj)
    db.commit()


# ----------------------------
# ODDS HISTORY
# ----------------------------

def log_odds(event_name, bookmaker, odds):
    obj = OddsHistory(
        event=event_name,
        book=bookmaker,
        odds=odds
    )
    db.add(obj)
    db.commit()


# ----------------------------
# LIVE STAT HISTORY
# ----------------------------

def log_live_stats(event_id, stats):
    obj = LiveStatsHistory(
        event_id=event_id,
        stats=stats
    )
    db.add(obj)
    db.commit()
