from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .strategy import ClosingPriceStrategy
from .scheduler import scheduler
from .hantu_stock import HantuStock

router = APIRouter(prefix="/bot", tags=["stock-bot"])

# 전역 HantuStock 인스턴스
hantu_stock = HantuStock()

@router.get("/balance")
def get_balance():
    """국내 주식 잔고 조회"""
    balance = hantu_stock.get_balance()
    if balance is None:
        raise HTTPException(status_code=500, detail="Failed to fetch domestic balance")
    return balance

@router.get("/overseas/balance")
def get_overseas_balance():
    """해외 주식 잔고 조회 (미국장 기준)"""
    balance = hantu_stock.get_overseas_balance()
    if balance is None:
        raise HTTPException(status_code=500, detail="Failed to fetch overseas balance")
    return balance

@router.post("/overseas/order")
def order_overseas_stock(ticker: str, type: str, qty: int, price: float, exchange_cd: str = "NAS"):
    """
    해외 주식 주문 (테스트용)
    type: 'buy' | 'sell'
    exchange_cd: 'NAS'(나스닥), 'NYS'(뉴욕), 'AMS'(아멕스)
    """
    result = hantu_stock.order_overseas(ticker, type, qty, price, exchange_cd)
    if result:
        return {"status": "success", "order_id": result}
    else:
        raise HTTPException(status_code=500, detail="Overseas order failed")

@router.post("/execute-strategy")
def execute_strategy_manually(db: Session = Depends(get_db)):
    """
    전략을 수동으로 즉시 실행합니다. (테스트용)
    """
    strategy = ClosingPriceStrategy(db)
    try:
        strategy.execute()
        return {"status": "executed", "message": "Strategy executed successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
