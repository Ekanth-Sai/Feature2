from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class QueryRequest(BaseModel):
    query: str
    user_id: Optional[int] = None

class StockDetail(BaseModel):
    symbol: str
    name: str
    price: float
    change: float
    volume: int
    market_cap: float

class HistoricalData(BaseModel):
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int

class MarketDataRequest(BaseModel):
    symbols: List[str]

class ScreenerResponse(BaseModel):
    query: str
    filters: Dict[str, Any]
    results: List[StockDetail]
    count: int
    execution_time: float
    timestamp: datetime

class SavedScreenerCreate(BaseModel):
    name: str
    query: str
    filters: Dict[str, Any]

class SavedScreenerUpdate(BaseModel):
    name: Optional[str] = None
    query: Optional[str] = None
    filters: Optional[Dict[str, Any]] = None

class SavedScreenerResponse(SavedScreenerCreate):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
