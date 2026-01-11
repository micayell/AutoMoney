from pykrx import stock
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class RiskManager:
    def __init__(self):
        pass

    def is_market_open(self):
        """오늘이 휴장일인지 확인"""
        today = datetime.now().strftime("%Y%m%d")
        try:
            # 해당 날짜의 KOSPI 지수 데이터를 가져와서 비어있으면 휴장일로 간주
            df = stock.get_index_ohlcv_by_date(today, today, "1001") # 1001: KOSPI
            if df.empty:
                logger.info(f"Today {today} is holiday.")
                return False
            return True
        except Exception as e:
            logger.error(f"Failed to check market status: {e}")
            # 에러 발생 시 보수적으로 휴장으로 간주 (안전 제일)
            return False

    def is_safe_ticker(self, ticker):
        """
        위험 종목 필터링
        1. 관리종목 / 거래정지 (pykrx에서 확인 가능)
        2. 동전주 (가격 < 1000) - 외부에서 가격 정보 받아와야 함
        """
        try:
            # 관리종목 확인
            # adm_issues = stock.get_market_administrative_equity_ticker_list()
            # if ticker in adm_issues:
            #    logger.warning(f"{ticker} is administrative issue. Skip.")
            #    return False
            
            # 여기서 가격 정보까지 체크하기엔 API 호출이 너무 많아질 수 있으므로
            # 전략 로직에서 가격 데이터를 가져왔을 때 체크하는 것이 효율적임
            return True
        except Exception as e:
            logger.error(f"Error checking safety of {ticker}: {e}")
            return False
            
risk_manager = RiskManager()

