from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from .strategy import ClosingPriceStrategy
from ..database import SessionLocal
import logging

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()

def run_strategy_job():
    """
    스케줄러에 의해 호출되는 래퍼 함수
    """
    db = SessionLocal()
    try:
        strategy = ClosingPriceStrategy(db)
        strategy.execute()
    except Exception as e:
        logger.error(f"Strategy job failed: {e}")
    finally:
        db.close()

def start_scheduler():
    # 매일 평일 15:20에 실행
    trigger = CronTrigger(day_of_week='mon-fri', hour='15', minute='20')
    
    scheduler.add_job(run_strategy_job, trigger, id='closing_price_strategy')
    scheduler.start()
    logger.info("Stock trading scheduler started (15:20 daily).")
