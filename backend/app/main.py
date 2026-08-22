import time
import os
import spacy
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from app.config import settings
from app.exceptions import AppException
from app.responses import error_response, success_response
from app.database.mongodb import connect_db, disconnect_db, create_indexes
from app.routers.auth import router as auth_router
from app.routers.resume import router as resume_router
from app.routers.analysis import router as analysis_router

# Setup Loguru logger
import sys
logger.remove()  # Remove default handler
# Console handler: INFO level
logger.add(
    sys.stderr,
    level="INFO",
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)
# File handler: DEBUG level, daily rotation, 7-day retention
os.makedirs("logs", exist_ok=True)
logger.add(
    "logs/app.log",
    rotation="00:00",
    retention="7 days",
    level="DEBUG",
    enqueue=True,
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}"
)

# Global objects
spacy_model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    logger.info("Application starting up...")
    
    # Load spacy model
    global spacy_model
    try:
        logger.info("Loading spaCy model en_core_web_sm...")
        spacy_model = spacy.load("en_core_web_sm")
        logger.info("spaCy model loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to load spaCy model: {e}")
        # In production, we might want to fail fast if AI is required
        # raise e
    
    # Create upload directory
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    logger.info(f"Upload directory ensured at {settings.UPLOAD_DIR}")
    
    # Connect to MongoDB
    await connect_db()
    await create_indexes()
    
    yield
    
    # Shutdown actions
    logger.info("Application shutting down...")
    await disconnect_db()

app = FastAPI(
    title="AI Resume Analyzer & Role Fit System API",
    description="API for parsing resumes and calculating role fit.",
    version="1.0.0",
    lifespan=lifespan
)

# Middleware: CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL, 
        "http://localhost:5173", 
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware: Logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    method = request.method
    path = request.url.path
    
    logger.info(f"Request started: {method} {path}")
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"Request completed: {method} {path} - Status: {response.status_code} - Duration: {process_time:.4f}s")
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.exception(f"Request failed: {method} {path} - Duration: {process_time:.4f}s - Error: {str(e)}")
        raise

# Exception handlers
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    logger.error(f"AppException: {exc.error_code} - {exc.detail}")
    return error_response(
        message=exc.detail,
        error_code=exc.error_code,
        status_code=exc.status_code
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {str(exc)}")
    return error_response(
        message="An unexpected error occurred.",
        error_code="INTERNAL_SERVER_ERROR",
        status_code=500
    )

# Router registration
app.include_router(auth_router)
app.include_router(resume_router)
app.include_router(analysis_router)

@app.get("/api/health", tags=["system"])
async def health_check():
    return success_response(data={"status": "healthy"}, message="Service is up and running.")
