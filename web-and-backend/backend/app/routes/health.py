from fastapi import APIRouter
from app.core.config import settings

router = APIRouter(tags=["Health"])


@router.get("/health")
def health():
    return {
        "status": "ok",
        "service": "MandiMitra Backend",
        "data_api_configured": bool(settings.data_gov_api_key),
    }
