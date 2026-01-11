from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from .stats import calculate_portfolio_stats

router = APIRouter(prefix="/analysis", tags=["analysis"])

class AssetValue(BaseModel):
    date: str
    value: float

class PortfolioRequest(BaseModel):
    history: List[AssetValue]

@router.post("/portfolio")
def analyze_portfolio(request: PortfolioRequest):
    data = [item.dict() for item in request.history]
    try:
        result = calculate_portfolio_stats(data)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

