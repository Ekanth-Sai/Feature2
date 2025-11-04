from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import time
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.pydantic_models import (
    QueryRequest, ScreenerResponse, StockDetail,
    SavedScreenerCreate, SavedScreenerResponse, SavedScreenerUpdate
)
from app.models.database_models import SavedScreener, QueryLog
from app.services.nlp_parser import NLPQueryParser
from app.services.screener import StockScreener
from app.services.data_provider import get_data_provider

router = APIRouter()

@router.post("/screen", response_model=ScreenerResponse)
async def screen_stocks(
    request: QueryRequest,
    db: Session = Depends(get_db)
):
    start_time = time.time()
    
    try:
        parser = NLPQueryParser()
        filters = await parser.parse_query(request.query)
        
        provider = get_data_provider()
        df = provider.generate_mock_data(100)  # In production, use real data
        
        filtered_df = StockScreener.apply_filters(df, filters)
        
        results = [
            StockDetail(**row.to_dict())
            for _, row in filtered_df.iterrows()
        ]
        
        execution_time = time.time() - start_time
        
        query_log = QueryLog(
            user_id=request.user_id,
            query=request.query,
            filters=filters,
            result_count=len(results),
            execution_time=execution_time
        )
        db.add(query_log)
        db.commit()
        
        return ScreenerResponse(
            query=request.query,
            filters=filters,
            results=results[:50],  
            count=len(results),
            execution_time=execution_time,
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Screening failed: {str(e)}"
        )


@router.get("/saved", response_model=List[SavedScreenerResponse])
async def get_saved_screeners(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    screeners = db.query(SavedScreener).filter(
        SavedScreener.user_id == current_user["user_id"]
    ).all()
    
    return screeners


@router.post("/saved", response_model=SavedScreenerResponse)
async def save_screener(
    screener: SavedScreenerCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_screener = SavedScreener(
        user_id=current_user["user_id"],
        **screener.dict()
    )
    db.add(db_screener)
    db.commit()
    db.refresh(db_screener)
    
    return db_screener


@router.put("/saved/{screener_id}", response_model=SavedScreenerResponse)
async def update_screener(
    screener_id: int,
    screener: SavedScreenerUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_screener = db.query(SavedScreener).filter(
        SavedScreener.id == screener_id,
        SavedScreener.user_id == current_user["user_id"]
    ).first()
    
    if not db_screener:
        raise HTTPException(status_code=404, detail="Screener not found")
    
    for key, value in screener.dict(exclude_unset=True).items():
        setattr(db_screener, key, value)
    
    db.commit()
    db.refresh(db_screener)
    
    return db_screener


@router.delete("/saved/{screener_id}")
async def delete_screener(
    screener_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_screener = db.query(SavedScreener).filter(
        SavedScreener.id == screener_id,
        SavedScreener.user_id == current_user["user_id"]
    ).first()
    
    if not db_screener:
        raise HTTPException(status_code=404, detail="Screener not found")
    
    db.delete(db_screener)
    db.commit()
    
    return {"message": "Screener deleted successfully"}