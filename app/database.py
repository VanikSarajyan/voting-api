from functools import lru_cache
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import Settings


@lru_cache
def get_settings():
    return Settings()


s = get_settings()

DB_URL = f"postgresql://{s.db_username}:{s.db_password}@{s.db_hostname}:{s.db_port}/{s.db_name}"

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
