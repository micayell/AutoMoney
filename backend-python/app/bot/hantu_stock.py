import pandas as pd
import time
import requests
import json
import logging
import os
import FinanceDataReader as fdr
from pykrx import stock as pystock
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HantuStock:
    def __init__(self):
        # 환경변수에서 모드 읽어오기 (기본값 MOCK)
        self.mode = os.getenv("KIS_MODE", "MOCK").upper()
        
        if self.mode == "REAL":
            self._api_key = os.getenv("REAL_APP_KEY")
            self._secret_key = os.getenv("REAL_APP_SECRET")
            self._account_id = os.getenv("REAL_ACCOUNT_NO")
            self._base_url = 'https://openapi.koreainvestment.com:9443' # 실전 서버
            logger.info(">>> Running in REAL INVESTMENT mode <<<")
        else:
            self._api_key = os.getenv("MOCK_APP_KEY")
            self._secret_key = os.getenv("MOCK_APP_SECRET")
            self._account_id = os.getenv("MOCK_ACCOUNT_NO")
            self._base_url = 'https://openapivts.koreainvestment.com:29443' # 모의 서버
            logger.info(">>> Running in MOCK INVESTMENT mode <<<")

        self._account_suffix = "01"
        
        # Access Token 초기화
        self._access_token = self.get_access_token()

    def get_access_token(self):
        while True:
            try:
                headers = {"content-type":"application/json"}
                body = {
                    "grant_type":"client_credentials",
                    "appkey":self._api_key, 
                    "appsecret":self._secret_key,
                }
                url = f"{self._base_url}/oauth2/tokenP"
                res = requests.post(url, headers=headers, data=json.dumps(body))
                data = res.json()
                
                if 'access_token' in data:
                    logger.info("Access token acquired successfully.")
                    return data['access_token']
                else:
                    logger.error(f"Failed to get access token: {data}")
                    time.sleep(10)
            except Exception as e:
                logger.error(f"Error getting access token: {e}")
                time.sleep(10)

    def get_header(self, tr_id):
        return {
            "content-type": "application/json",
            "appkey": self._api_key, 
            "appsecret": self._secret_key,
            "authorization": f"Bearer {self._access_token}",
            "tr_id": tr_id,
        }

    def _requests(self, url, headers, params, request_type='get'):
        while True:
            try:
                if request_type == 'get':
                    response = requests.get(url, headers=headers, params=params)
                else:
                    response = requests.post(url, headers=headers, data=json.dumps(params))
                
                contents = response.json()
                
                if contents.get('rt_cd') != '0':
                    # 초당 거래건수 초과 에러 처리
                    if contents.get('msg_cd') == 'EGW00201': 
                        time.sleep(0.2)
                        continue
                    else:
                        logger.error(f"API Error: {contents.get('msg1')} (Code: {contents.get('msg_cd')})")
                
                return response.headers, contents
            except Exception as e:
                logger.error(f"Request failed: {e}")
                time.sleep(1)

    # --- Market Data ---
    def get_past_data(self, ticker, n=100):
        temp = fdr.DataReader(ticker)
        temp.columns = [col.lower() for col in temp.columns]
        temp.index.name = 'timestamp'
        # Reset index to make timestamp a column if needed, or keep as index
        return temp.tail(n)

    def get_market_ohlcv_by_date(self, date_str, market='ALL'):
        """
        특정 날짜의 전 종목 시세 조회 (pykrx)
        market: KOSPI, KOSDAQ, ALL
        """
        try:
            df = pystock.get_market_ohlcv(date_str, market=market)
            df = df.reset_index()
            # Standardize columns
            df.columns = ['ticker', 'open', 'high', 'low', 'close', 'volume', 'trade_amount', 'diff']
            return df
        except Exception as e:
            logger.error(f"Failed to get market data for {date_str}: {e}")
            return None

    # --- Domestic Account & Trading ---
    def get_balance(self):
        """국내 계좌 잔고 조회 (주식 + 예수금)"""
        headers = self.get_header('TTTC8434R') # 실전/모의 국내주식 잔고
        if self.mode == "MOCK":
             headers = self.get_header('VTTC8434R') # 모의투자는 TR ID가 다를 수 있음 (보통 V가 붙음)

        params = {
            "CANO": self._account_id,
            "ACNT_PRDT_CD": self._account_suffix,
            "AFHR_FLPR_YN": "N",
            "OFL_YN": "N",
            "INQR_DVSN": "01",
            "UNPR_DVSN": "01",
            "FUND_STTL_ICLD_YN": "N",
            "FNCG_AMT_AUTO_RDPT_YN": "N",
            "PRCS_DVSN": "01",
            "CTX_AREA_FK100": "",
            "CTX_AREA_NK100": ""
        }
        url = f"{self._base_url}/uapi/domestic-stock/v1/trading/inquire-balance"
        _, result = self._requests(url, headers, params)
        
        if result.get('rt_cd') != '0':
            return None
            
        output1 = result.get('output1', []) # 보유 주식 리스트
        output2 = result.get('output2', []) # 계좌 잔고 정보 (예수금 등)
        
        return {
            "stocks": output1,
            "cash": int(output2[0]['prvs_rcdl_excc_amt']) if output2 else 0 # 가수도 제외한 예수금
        }

    def order(self, ticker, type, qty, price=0):
        """
        국내 주식 주문 실행
        type: 'buy' (매수), 'sell' (매도)
        price: 0이면 시장가, 아니면 지정가
        """
        tr_id = 'TTTC0802U' if type == 'buy' else 'TTTC0801U' 
        if self.mode == "MOCK":
            tr_id = 'VTTC0802U' if type == 'buy' else 'VTTC0801U'

        headers = self.get_header(tr_id)
        
        ord_dvsn = '01' if price == 0 else '00' # 01: 시장가, 00: 지정가
        
        params = {
            "CANO": self._account_id,
            "ACNT_PRDT_CD": self._account_suffix,
            "PDNO": ticker,
            "ORD_DVSN": ord_dvsn,
            "ORD_QTY": str(qty),
            "ORD_UNPR": str(price)
        }
        
        url = f"{self._base_url}/uapi/domestic-stock/v1/trading/order-cash"
        _, result = self._requests(url, headers, params, request_type='post')
        
        if result.get('rt_cd') == '0':
            logger.info(f"Order success: {type} {ticker} {qty}ea")
            return result.get('output', {}).get('ODNO') # 주문번호 리턴
        else:
            logger.error(f"Order failed: {result.get('msg1')}")
            return None

    # --- Overseas Account & Trading (New) ---
    def get_overseas_balance(self, exchange_cd="NAS"):
        """해외 주식 잔고 조회 (미국장 기준)"""
        # 해외 주식 잔고 조회 TR ID는 실전/모의 다를 수 있음
        tr_id = 'TTTS3012R' if self.mode == 'REAL' else 'VTTS3012R' # 해외주식 잔고
        
        headers = self.get_header(tr_id)
        params = {
            "CANO": self._account_id,
            "ACNT_PRDT_CD": self._account_suffix,
            "OVRS_EXCG_CD": exchange_cd, # NAS: 나스닥, NYS: 뉴욕, AMS: 아멕스
            "TR_CRCY_CD": "USD",
            "CTX_AREA_FK200": "",
            "CTX_AREA_NK200": ""
        }
        url = f"{self._base_url}/uapi/overseas-stock/v1/trading/inquire-balance"
        _, result = self._requests(url, headers, params)
        
        if result.get('rt_cd') != '0':
            return None
            
        output1 = result.get('output1', []) # 해외 주식 보유 내역
        output2 = result.get('output2', []) # 외화 예수금 내역
        
        return {
            "stocks": output1,
            "foreign_currency": output2
        }

    def order_overseas(self, ticker, type, qty, price, exchange_cd="NAS"):
        """
        해외 주식 주문 실행 (미국 주식)
        type: 'buy' (매수), 'sell' (매도)
        주의: 해외 주식은 시장가 주문 코드가 다를 수 있으며, 보통 지정가를 많이 사용함
        """
        tr_id = 'TTTS1002U' if type == 'buy' else 'TTTS1001U' # 실전 매수/매도
        if self.mode == 'MOCK':
            tr_id = 'VTTS1002U' if type == 'buy' else 'VTTS1001U' # 모의 매수/매도

        headers = self.get_header(tr_id)
        
        ord_dvsn = '00' # 지정가 (해외주식은 보통 지정가)
        
        params = {
            "CANO": self._account_id,
            "ACNT_PRDT_CD": self._account_suffix,
            "OVRS_EXCG_CD": exchange_cd, # NAS, NYS, AMS
            "PDNO": ticker,
            "ORD_QTY": str(qty),
            "OVRS_ORD_UNPR": str(price),
            "ORD_DVSN": ord_dvsn
        }
        
        url = f"{self._base_url}/uapi/overseas-stock/v1/trading/order"
        _, result = self._requests(url, headers, params, request_type='post')
        
        if result.get('rt_cd') == '0':
             logger.info(f"Overseas Order success: {type} {ticker} {qty}ea")
             return result.get('output', {}).get('ODNO')
        else:
            logger.error(f"Overseas Order failed: {result.get('msg1')}")
            return None
