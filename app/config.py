from pydantic_settings import BaseSettings
from typing import Any, Dict, Optional
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

class Settings(BaseSettings):
    database_url: str = os.environ.get("DATABASE_URL")
    jwt_secret_key: str = os.environ.get("JWT_SECRET_KEY")

    class Config:
        env_file = ".env"

settings = Settings()

# ... other database config

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()