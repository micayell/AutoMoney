import pandas as pd
from datetime import datetime
import logging
from sqlalchemy.orm import Session
from .hantu_stock import HantuStock
from .models import BotState, TradeLog, TradeStatus
from .risk_manager import risk_manager

logger = logging.getLogger(__name__)

class ClosingPriceStrategy:
    def __init__(self, db: Session):
        self.ht = HantuStock()
        self.db = db

    def execute(self):
        """
        15:20분에 실행될 메인 로직
        """
        logger.info("Executing Closing Price Strategy...")

        # 1. 휴장일 체크
        if not risk_manager.is_market_open():
            logger.info("Today is holiday. Skip strategy.")
            return

        # 2. 보유 종목 관리 (매도 조건 체크)
        self.manage_holdings()

        # 3. 신규 매수 (매수 조건 체크)
        self.find_and_buy()

    def manage_holdings(self):
        """보유 기간 3일 지난 종목 매도"""
        states = self.db.query(BotState).filter(BotState.status == TradeStatus.HOLDING).all()
        
        # 실제 계좌 잔고 확인
        balance = self.ht.get_balance()
        if not balance:
            logger.error("Failed to get balance. Skip managing holdings.")
            return
            
        real_holdings = {item['pdno']: int(item['hldg_qty']) for item in balance['stocks']}
        
        for state in states:
            # DB에는 있는데 실제 계좌에 없으면 DB 정리 (동기화)
            if state.ticker not in real_holdings:
                logger.warning(f"Ticker {state.ticker} not found in real account. Removing from DB.")
                self.db.delete(state)
                continue

            # 보유 기간 증가 (하루가 지났다고 가정 - 실제로는 날짜 비교가 더 정확함)
            # 여기서는 스케줄러가 하루 한 번 도니까 단순 증가
            state.holding_period += 1
            
            # 3일차면 매도 (인프런 강의 로직: holding_period >= 3)
            if state.holding_period >= 3:
                logger.info(f"Selling {state.ticker} (Held for {state.holding_period} days)")
                qty = real_holdings[state.ticker]
                
                order_id = self.ht.order(state.ticker, 'sell', qty, 0) # 시장가 매도
                
                if order_id:
                    state.status = TradeStatus.SOLD
                    # 로그 기록
                    self.db.add(TradeLog(
                        ticker=state.ticker, action="SELL", qty=qty, 
                        price=0, reason="Time limit reached"
                    ))
        
        self.db.commit()

    def find_and_buy(self):
        """
        조건: 
        1. 최근 5일 종가 중 오늘 종가가 최저
        2. 20일 이동평균선 > 오늘 종가 (역추세)
        3. 거래량 상위 10개
        """
        today = datetime.now().strftime("%Y%m%d")
        
        # 전체 종목 시세 가져오기 (시간 소요됨)
        # 인프런 강의에서는 get_past_data_total 사용 -> 여기서는 pykrx 직접 활용
        logger.info("Fetching market data...")
        # pykrx의 get_market_ohlcv_by_date 사용 (오늘자)
        # 하지만 5일치 데이터가 필요하므로, 여기서는 시간 관계상 
        # KOSPI/KOSDAQ 상위 거래대금 종목 50개를 추려서 각각 분석하는 것이 현실적임
        # (전 종목 20일치 데이터를 다 가져오면 API 제한 걸릴 수 있음)
        
        # 1. 거래대금 상위 50개 선정
        df_today = self.ht.get_market_ohlcv_by_date(today, "KOSPI") # 일단 코스피만
        if df_today is None: return

        top_volume = df_today.sort_values('trade_amount', ascending=False).head(50)
        
        candidates = []
        
        for index, row in top_volume.iterrows():
            ticker = row['ticker']
            
            # 위험 종목 필터링 (동전주 제외)
            if row['close'] < 1000: continue
            
            # 2. 과거 데이터 조회 (20일치)
            past_data = self.ht.get_past_data(ticker, n=21) # 오늘 포함 여부 확인 필요
            
            if len(past_data) < 20: continue
            
            close_prices = past_data['close']
            
            # 오늘 종가 (장중이면 현재가)
            today_close = close_prices.iloc[-1]
            
            # 5일 최저가 체크
            min_5d = close_prices.tail(5).min()
            
            # 20일 이평선
            ma_20 = close_prices.tail(20).mean()
            
            # 조건 만족?
            if today_close == min_5d and today_close < ma_20:
                candidates.append(ticker)
                if len(candidates) >= 5: break # 최대 5개까지만 매수
        
        # 3. 매수 실행
        for ticker in candidates:
            # 이미 보유중인지 체크
            exists = self.db.query(BotState).filter(
                BotState.ticker == ticker, 
                BotState.status == TradeStatus.HOLDING
            ).first()
            if exists: continue
            
            logger.info(f"Buying {ticker} (Condition matched)")
            
            # 수량 계산 (예: 1주 - 자금 관리 로직 필요)
            qty = 1 
            
            order_id = self.ht.order(ticker, 'buy', qty, 0)
            
            if order_id:
                # DB 저장
                new_state = BotState(
                    ticker=ticker,
                    holding_period=0,
                    avg_price=0, # 체결가 나중에 확인 필요하지만 일단 0
                    qty=qty,
                    status=TradeStatus.HOLDING
                )
                self.db.add(new_state)
                self.db.add(TradeLog(
                    ticker=ticker, action="BUY", qty=qty, 
                    price=0, reason="Closing Price Strategy"
                ))
        
        self.db.commit()

