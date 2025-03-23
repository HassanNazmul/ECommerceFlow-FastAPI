# authentication/main.py
from fastapi import FastAPI
from dotenv import load_dotenv

from authentication.core.config import settings
from authentication.api.v1.endpoints.auth import router as auth_router

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
)

# Include routes
app.include_router(auth_router, prefix="/auth", tags=["auth"])
