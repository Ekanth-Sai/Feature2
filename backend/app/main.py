from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import logging
import time

from app.core.config import settings
from app.core.database import DatabaseService, engine
from app.models.database_models import Base

from app.api.routes import screener, stocks, auth, websocket

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting AI Stock Screener API")
    
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")

    if DatabaseService.check_connection():
        logger.info("Database connection established")
    else:
        logger.error("Failed to connect to database")
    
    yield
    
    logger.info("Shutting down AI Stock Screener API")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered stock screening with natural language queries",
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def error_handling(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logger.error(f"Unhandled error: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "Internal server error",
                "error": str(e) if settings.DEBUG else "An error occurred"
            }
        )

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    logger.info(f"Request: {request.method} {request.url.path}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(
        f"Response: {response.status_code} | "
        f"Time: {process_time:.3f}s | "
        f"Path: {request.url.path}"
    )
    
    response.headers["X-Process-Time"] = str(process_time)
    
    return response

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "errors": exc.errors()
        }
    )

@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "environment": settings.ENVIRONMENT,
        "docs": "/docs" if settings.DEBUG else "Documentation disabled in production"
    }


@app.get("/health")
async def health_check():
    db_status = DatabaseService.check_connection()
    
    return {
        "status": "healthy" if db_status else "unhealthy",
        "database": "connected" if db_status else "disconnected",
        "version": settings.APP_VERSION
    }


@app.get("/api/status")
async def api_status():
    return {
        "api_version": "v1",
        "status": "operational",
        "features": {
            "natural_language_queries": True,
            "real_time_data": True,
            "technical_indicators": True,
            "saved_screeners": True,
            "alerts": True,
            "websocket": True
        }
    }

app.include_router(
    screener.router,
    prefix=f"{settings.API_V1_PREFIX}/screener",
    tags=["Screener"]
)

app.include_router(
    stocks.router,
    prefix=f"{settings.API_V1_PREFIX}/stocks",
    tags=["Stocks"]
)

app.include_router(
    auth.router,
    prefix=f"{settings.API_V1_PREFIX}/auth",
    tags=["Authentication"]
)

app.include_router(
    websocket.router,
    prefix="/ws",
    tags=["WebSocket"]
)

@app.get(f"{settings.API_V1_PREFIX}/markets/status")
async def market_status():
    from datetime import datetime
    import pytz
    
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    hour = now.hour
    minute = now.minute
    day_of_week = now.weekday()
    
    # Market hours: 9:15 AM to 3:30 PM IST, Monday to Friday
    is_open = (
        day_of_week < 5 and  # Monday to Friday
        (hour > 9 or (hour == 9 and minute >= 15)) and
        (hour < 15 or (hour == 15 and minute <= 30))
    )
    
    return {
        "market": "NSE",
        "is_open": is_open,
        "current_time": now.isoformat(),
        "timezone": "Asia/Kolkata",
        "trading_hours": "9:15 AM - 3:30 PM IST",
        "trading_days": "Monday - Friday"
    }


@app.get(f"{settings.API_V1_PREFIX}/analytics/popular-queries")
async def get_popular_queries():
    from app.core.database import get_db
    from app.models.database_models import QueryLog
    from sqlalchemy import func
    
    return {
        "popular_queries": [
            "banking stocks with RSI below 30",
            "midcap stocks near 52-week high",
            "IT stocks with high volume",
            "pharma stocks with positive momentum"
        ]
    }


@app.get(f"{settings.API_V1_PREFIX}/analytics/trending-sectors")
async def get_trending_sectors():
    return {
        "trending_sectors": [
            {"sector": "Banking", "change": 2.5, "volume_increase": 35},
            {"sector": "IT", "change": 1.8, "volume_increase": 28},
            {"sector": "Pharma", "change": -0.5, "volume_increase": 15}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )