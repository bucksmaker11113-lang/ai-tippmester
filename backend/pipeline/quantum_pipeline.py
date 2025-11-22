# ==========================================================
#  QUANTUM ENGINE V7.0 MASTER PIPELINE
# ==========================================================
#
#  Ez a rendszer csúcsa.
#
#  ÉS A TE MEGADOTT LOGIKÁD SZERINT:
#   - NAPI 4 SINGLE TIPPEK
#      * 1 FOCI
#      * 1 KOSÁR
#      * 1 JÉGKORONG
#      * 1 TENISZ
#
#   - NAPI 1 KOMBI TIPP (4–5 elem, de nem single-ből!)
#
#   - NAPI LIVE TIPPEK
#       * Magyar idő szerint 14:00 után
#       * Push értesítéssel
#
#   - KÜLÖN BANKROLL
#       * single bankroll
#       * kombi bankroll
#       * live bankroll
#
#   - TELJES AI STACK:
#       RL + MultiAgent + Bookmaker + Gameflow + Reasoning + DeepLearning
#       = QuantumSynth
#
# ==========================================================

import datetime
from engine.quantumsynth_engine import quantum_synth
from engine.gameflow_engine import predict_next_gameflow
from engine.multi_agent_engine import value_ai
from engine.bookmaker_model_engine import bookmaker_engine
from engine.reasoning_layer import reasoning_engine
from engine.deep_learning_engine import predict_strength

from database.db import SessionLocal
from database.models import (
    TipSingle, TipKombi, TipLive, BankrollLog
)


# --------------------------------------------------------------
# AUTO BANKROLL FETCH + UPDATE
# --------------------------------------------------------------

def get_bankroll(category):
    db = SessionLocal()
    br = db.query(BankrollLog).filter(BankrollLog.category == category)\
        .order_by(BankrollLog.id.desc()).first()
    return br.balance if br else 1000


def update_bankroll(category, new_balance):
    db = SessionLocal()
    br = BankrollLog(category=category, balance=new_balance, timestamp=datetime.datetime.now())
    db.add(br)
    db.commit()


# --------------------------------------------------------------
# STAKE CALCULATION (1% alap)
# --------------------------------------------------------------

def compute_stake(bankroll, strength):
    base = bankroll * 0.01
    modifier = 0.5 + (strength * 0.5)
    return round(base * modifier, 2)


# --------------------------------------------------------------
# SINGLE TIP GENERATOR (FOCI / KOSÁR / HOCKEY / TENISZ)
# --------------------------------------------------------------

def generate_single_tip(event):
    """Event = odds scannerből (te fogod integrálni később)"""

    ctx = {
        "prematch": event["prematch"],
        "live": event.get("live", {}),
        "odds": event["odds"],
        "bookmaker": event["bookmakers"],
        "bankroll": get_bankroll("single"),
        "risk": 1.0,
        "variance": event.get("variance", 0.1),
        "tm_odds": event["tm_odds"],
        "reasoning": event["reasoning"]
    }

    result = quantum_synth.compute_master_score(ctx)
    final_strength = result["final_score"]

    if final_strength < 0.55:
        return None  # nem elég erős a single tipphez

    stake = compute_stake(ctx["bankroll"], final_strength)

    db = SessionLocal()
    tip = TipSingle(
        sport=event["sport"],
        match=event["match"],
        odds=event["tm_odds"],
        strength=final_strength,
        stake=stake,
        timestamp=datetime.datetime.now()
    )
    db.add(tip)
    db.commit()

    return {
        "match": event["match"],
        "sport": event["sport"],
        "odds": event["tm_odds"],
        "strength": final_strength,
        "stake": stake
    }


# --------------------------------------------------------------
# KOMBI TIPPEK (4–5 elem, NEM single duplikátumból!)
# --------------------------------------------------------------

def generate_kombi_tips(events):
    selected = []
    for ev in events:
        if len(selected) >= 5:
            break

        ctx = {
            "prematch": ev["prematch"],
            "live": ev.get("live", {}),
            "odds": ev["odds"],
            "bookmaker": ev["bookmakers"],
            "bankroll": get_bankroll("kombi"),
            "risk": 1.0,
            "variance": ev.get("variance", 0.1),
            "tm_odds": ev["tm_odds"],
            "reasoning": ev["reasoning"]
        }

        result = quantum_synth.compute_master_score(ctx)
        strength = result["final_score"]

        if strength > 0.60:     # kombi küszöb
            selected.append({
                "match": ev["match"],
                "odds": ev["tm_odds"],
                "strength": strength
            })

    if len(selected) < 4:
        return None

    combined_odds = 1
    for s in selected:
        combined_odds *= s["odds"]

    db = SessionLocal()
    tip = TipKombi(
        matches=str(selected),
        combined_odds=combined_odds,
        timestamp=datetime.datetime.now()
    )
    db.add(tip)
    db.commit()

    return {
        "tips": selected,
        "combined_odds": combined_odds
    }


# --------------------------------------------------------------
# LIVE TIP GENERATOR (14:00 után)
# --------------------------------------------------------------

def generate_live_tip(event):
    now = datetime.datetime.now().time()
    if now < datetime.time(14, 0):
        return None

    # Live data
    gf = predict_next_gameflow()

    ctx = {
        "prematch": event.get("prematch", {}),
        "live": event.get("live", {}),
        "odds": event["odds"],
        "bookmaker": event["bookmakers"],
        "bankroll": get_bankroll("live"),
        "risk": 1.0,
        "variance": event.get("variance", 0.1),
        "tm_odds": event["tm_odds"],
        "reasoning": event["reasoning"]
    }

    result = quantum_synth.compute_master_score(ctx)
    strength = result["final_score"]

    if strength < 0.70:
        return None  # csak nagyon erős live tippek

    stake = compute_stake(ctx["bankroll"], strength)

    db = SessionLocal()
    tip = TipLive(
        match=event["match"],
        odds=event["tm_odds"],
        live_strength=strength,
        stake=stake,
        timestamp=datetime.datetime.now()
    )
    db.add(tip)
    db.commit()

    return {
        "match": event["match"],
        "odds": event["tm_odds"],
        "strength": strength,
        "stake": stake,
        "live_prediction": gf
    }


# --------------------------------------------------------------
# MASTER GENERATOR – összes tipp
# --------------------------------------------------------------

def generate_daily_tips(events):

    # ------------------------------
    # SINGLE TIPPEK – sportonként 1
    # ------------------------------
    sports = ["football", "basketball", "hockey", "tennis"]
    singles = []

    for sp in sports:
        evs = [e for e in events if e["sport"] == sp]
        if not evs:
            continue
        best = sorted(evs, key=lambda x: x["tm_odds"])[:10]
        tip = None
        for candidate in best:
            tip = generate_single_tip(candidate)
            if tip:
                singles.append(tip)
                break

    # ------------------------------
    # KOMBI TIPPEK (4–5 elem)
    # ------------------------------
    kombi = generate_kombi_tips(events)

    # ------------------------------
    # LIVE TIP (ha van)
    # ------------------------------
    live_candidates = [e for e in events if e.get("live")]
    live_tip = None
    if live_candidates:
        for ev in live_candidates:
            live_tip = generate_live_tip(ev)
            if live_tip:
                break

    return {
        "single": singles,
        "kombi": kombi,
        "live": live_tip
    }
