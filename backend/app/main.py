from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.middleware.exception_handler import GlobalExceptionMiddleware
from app.middleware.logging_middleware import LoggingMiddleware
from app.routers import auth

app = FastAPI(
    title="Whittaker Agency API",
    description="Insurance agency management system serving families and businesses across Oregon",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware
app.add_middleware(GlobalExceptionMiddleware)
app.add_middleware(LoggingMiddleware)

# Routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])


@app.get("/")
async def root():
    return {
        "message": "Whittaker Agency API",
        "version": "1.0.0",
        "tagline": "Your Family, Your Business, Our Priority"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
