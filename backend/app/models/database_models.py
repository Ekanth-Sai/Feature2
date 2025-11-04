from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class StockData(Base):
    __tablename__ = "stock_data"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True, nullable=False)
    name = Column(String)
    price = Column(Float)
    change = Column(Float)
    volume = Column(Integer)
    market_cap = Column(Float)
    sector = Column(String, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class SavedScreener(Base):
    __tablename__ = "saved_screeners"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    name = Column(String, nullable=False)
    query = Column(String, nullable=False)
    filters = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class QueryLog(Base):
    __tablename__ = "query_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    query = Column(String, nullable=False)
    filters = Column(JSON)
    result_count = Column(Integer)
    execution_time = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())