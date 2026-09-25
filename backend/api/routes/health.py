from fastapi import APIRouter

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
