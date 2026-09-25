from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from backend.api.schemas.database import DatabaseHealthResponse
from backend.db.session import get_db

router = APIRouter(tags=["Health & Service Info"])


@router.get("/health", summary="Health Check")
def health_check():
    """Returns service health status."""
    return {"status": "ok", "service": "FRADMS API"}


@router.get("/", summary="API Root Info")
def root_info():
    """Returns API service description and sitemap."""
    return {
        "service": "Fair Resource Allocation & Dynamic Matching System API",
        "version": "1.0.0",
        "documentation": "/docs",
        "redoc": "/redoc",
        "status": "healthy",
    }


@router.get(
    "/api/v1/database/health",
    response_model=DatabaseHealthResponse,
    summary="Database Connectivity Health Check",
    tags=["Database Persistence"],
)
def database_health_check(db: Session = Depends(get_db)):
    """Verifies that the application can connect to PostgreSQL/database."""
    try:
        db.execute(text("SELECT 1"))
        return DatabaseHealthResponse(status="ok", database="postgresql")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection error: {str(e)}",
        )
