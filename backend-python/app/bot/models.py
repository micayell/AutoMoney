from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from sqlalchemy.sql import func
import enum
from ..database import Base

class TradeStatus(str, enum.Enum):
    BUYING = "BUYING"
    HOLDING = "HOLDING"
    SELLING = "SELLING"
    SOLD = "SOLD"

class BotState(Base):
    """
    현재 봇이 보유 중인 종목의 상태를 관리하는 테이블
    (strategy_data.json 대체)
    """
    __tablename__ = "bot_states"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, unique=True, index=True) # 종목코드
    holding_period = Column(Integer, default=0) # 보유 일수
    avg_price = Column(Float) # 평단가
    qty = Column(Integer) # 보유 수량
    status = Column(String, default=TradeStatus.HOLDING) # 상태
    last_updated = Column(DateTime(timezone=True), onupdate=func.now(), default=func.now())

class TradeLog(Base):
    """
    매매 이력을 기록하는 테이블 (복기용)
    """
    __tablename__ = "trade_logs"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String)
    action = Column(String) # BUY / SELL
    price = Column(Float)
    qty = Column(Integer)
    reason = Column(String) # 매매 사유 (예: 5일선 돌파)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

