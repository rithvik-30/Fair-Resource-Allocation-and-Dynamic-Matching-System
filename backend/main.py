from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.api.routes.allocation import router as allocation_router
from backend.api.routes.dispatch import router as dispatch_router
from backend.api.routes.health import router as health_router
from backend.api.routes.simulation import router as simulation_router

app = FastAPI(
    title="FRADMS API",
    description=(
        "FastAPI Backend for Fair Resource Allocation & Dynamic Matching System.\n"
        "Exposes algorithmic decision-support engines for food rescue logistics."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure Development CORS for Next.js frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(health_router)
app.include_router(allocation_router)
app.include_router(dispatch_router)
app.include_router(simulation_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Clean validation error response without leaking stack traces."""
    errors = []
    for err in exc.errors():
        loc_str = " -> ".join(str(loc) for loc in err.get("loc", []))
        msg = err.get("msg", "Validation error")
        errors.append({"location": loc_str, "message": msg})

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": True,
            "message": "Invalid request parameters or malformed input schema.",
            "details": errors,
        },
    )
