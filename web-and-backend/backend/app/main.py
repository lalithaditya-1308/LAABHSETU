from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import health, mandi, compare, metadata, assistant
from app.core.config import settings

app = FastAPI(
    title="MandiMitra Backend",
    description="Expense-aware mandi price comparison API for farmers.",
    version="0.1.0",
)

# For local development. In production, set FRONTEND_ORIGINS to your frontend URL(s).
origins = [origin.strip() for origin in settings.frontend_origins.split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1")
app.include_router(metadata.router, prefix="/api/v1")
app.include_router(mandi.router, prefix="/api/v1")
app.include_router(compare.router, prefix="/api/v1")
app.include_router(assistant.router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "Welcome to MandiMitra API", "docs": "/docs", "health": "/api/v1/health"}
