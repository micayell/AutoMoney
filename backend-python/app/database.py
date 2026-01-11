from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Docker Compose에서 설정한 DB 정보와 일치해야 함
# 로컬 개발 시에는 localhost, docker network 내부에서는 db 서비스명 사용 필요
# 여기서는 로컬 실행을 가정하여 localhost 사용
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://automoney:automoney_pass@localhost:5432/automoney")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

