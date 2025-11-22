from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.sql import func
from database.db import Base


class TipSingle(Base):
    __tablename__ = "tips_single"

    id = Column(Integer, primary_key=True, index=True)
    sport = Column(String)
    team1 = Column(String)
    team2 = Column(String)
    odds = Column(Float)
    strength = Column(Float)
    timestamp = Column(DateTime, server_default=func.now())


class TipKombi(Base):
    __tablename__ = "tips_kombi"

    id = Column(Integer, primary_key=True, index=True)
    events = Column(JSON)
    total_odds = Column(Float)
    strength = Column(Float)
    timestamp = Column(DateTime, server_default=func.now())


class TipLive(Base):
    __tablename__ = "tips_live"

    id = Column(Integer, primary_key=True, index=True)
    team1 = Column(String)
    team2 = Column(String)
    odds = Column(Float)
    momentum = Column(Float)
    live_strength = Column(Float)
    timestamp = Column(DateTime, server_default=func.now())


class BankrollLog(Base):
    __tablename__ = "bankroll_log"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String)  # single / kombi / live
    amount = Column(Float)
    balance = Column(Float)
    timestamp = Column(DateTime, server_default=func.now())


class OddsHistory(Base):
    __tablename__ = "odds_history"

    id = Column(Integer, primary_key=True, index=True)
    event = Column(String)
    book = Column(String)
    odds = Column(Float)
    timestamp = Column(DateTime, server_default=func.now())


class LiveStatsHistory(Base):
    __tablename__ = "live_stats_history"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer)
    stats = Column(JSON)
    timestamp = Column(DateTime, server_default=func.now())
