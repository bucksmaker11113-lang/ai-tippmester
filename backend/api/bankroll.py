from fastapi import APIRouter

router = APIRouter(prefix="/api/bankroll", tags=["bankroll"])

bankroll_single = 300000
bankroll_kombi = 300000
bankroll_live = 300000

@router.get("/single")
def get_single_bankroll():
    return {"bankroll": bankroll_single}

@router.get("/kombi")
def get_kombi_bankroll():
    return {"bankroll": bankroll_kombi}

@router.get("/live")
def get_live_bankroll():
    return {"bankroll": bankroll_live}
