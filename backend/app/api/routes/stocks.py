from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.models.pydantic_models import StockDetail, HistoricalData, MarketDataRequest
from app.models.database_models import StockData
from app.services.data_provider import get_data_provider

router = APIRouter()


@router.get("/", response_model=List[StockDetail])
async def get_all_stocks(
    limit: int = Query(100, ge=1, le=500),
    sector: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(StockData).order_by(StockData.timestamp.desc())
    
    if sector:
        query = query.filter(StockData.sector == sector)
    
    stocks = query.limit(limit).all()
    return stocks


@router.get("/{symbol}", response_model=StockDetail)
async def get_stock_detail(
    symbol: str,
    db: Session = Depends(get_db)
):
    stock = db.query(StockData).filter(
        StockData.symbol == symbol.upper()
    ).order_by(StockData.timestamp.desc()).first()
    
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    return stock


@router.get("/{symbol}/historical", response_model=List[HistoricalData])
async def get_historical_data(
    symbol: str,
    period: str = Query("1mo", regex="^(1d|5d|1mo|3mo|6mo|1y|2y|5y|max)$")
):
    provider = get_data_provider()
    
    try:
        df = provider.get_historical_data(symbol, period)
        
        data = []
        for index, row in df.iterrows():
            data.append(HistoricalData(
                date=index,
                open=row['Open'],
                high=row['High'],
                low=row['Low'],
                close=row['Close'],
                volume=int(row['Volume'])
            ))
        
        return data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch historical data: {str(e)}"
        )


@router.get("/sectors/list")
async def get_sectors():
    return {
        "sectors": ["Banking", "IT", "Pharma", "Auto", "FMCG", "Metals", "Energy", "Realty"]
    }


@router.post("/batch", response_model=List[StockDetail])
async def get_multiple_stocks(
    request: MarketDataRequest,
    db: Session = Depends(get_db)
):
    stocks = db.query(StockData).filter(
        StockData.symbol.in_(request.symbols)
    ).order_by(StockData.timestamp.desc()).all()
    
    return stocks

