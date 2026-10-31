from fastapi import APIRouter, HTTPException
from app.models.schemas import CompareRequest
from app.services.calculation_service import compare_mandis
from app.services.data_gov_client import DataGovAPIError

router = APIRouter(tags=["Net Return Comparison"])


@router.post("/compare")
def compare(request: CompareRequest):
    try:
        return compare_mandis(request)
    except DataGovAPIError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
