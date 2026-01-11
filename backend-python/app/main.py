from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from .bot import router as bot_router
from .analysis import router as analysis_router
from .analysis import lotto_router
from .bot.scheduler import start_scheduler
from contextlib import asynccontextmanager

# Create tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    start_scheduler()
    yield
    # Shutdown
    # scheduler.shutdown() if needed

app = FastAPI(title="AutoMoney Data & Bot Service", lifespan=lifespan)

app.include_router(bot_router.router)
app.include_router(analysis_router.router)
app.include_router(lotto_router.router)

@app.get("/")
def read_root():
    return {"message": "AutoMoney Python Service is running"}

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        # DB 연결 테스트
        db.execute("SELECT 1")
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

