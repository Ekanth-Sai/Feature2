from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator, Optional
import redis

from .config import settings
from app.models.database_models import Base

engine = create_engine(
    settings.DATABASE_URL,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    echo=settings.DEBUG
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

redis_client = redis.from_url(
    settings.REDIS_URL,
    encoding="utf-8",
    decode_responses=True
)

def get_redis() -> redis.Redis:
    return redis_client

class DatabaseService:
    @staticmethod
    def create_all_tables():
        Base.metadata.create_all(bind=engine)
    
    @staticmethod
    def drop_all_tables():
        Base.metadata.drop_all(bind=engine)
    
    @staticmethod
    def check_connection() -> bool:
        try:
            db = SessionLocal()
            db.execute("SELECT 1")
            db.close()
            return True
        except Exception:
            return False

class CacheService:
    def __init__(self):
        self.redis = redis_client
    
    def get(self, key: str) -> Optional[str]:
        return self.redis.get(key)
    
    def set(self, key: str, value: str, ttl: int = settings.CACHE_TTL):
        return self.redis.setex(key, ttl, value)
    
    def delete(self, key: str):
        return self.redis.delete(key)
    
    def exists(self, key: str) -> bool:
        return self.redis.exists(key) > 0
    
    def flush_all(self):
        return self.redis.flushall()
    
    def get_many(self, pattern: str):
        keys = self.redis.keys(pattern)
        if not keys:
            return {}
        values = self.redis.mget(keys)
        return dict(zip(keys, values))

cache_service = CacheService()