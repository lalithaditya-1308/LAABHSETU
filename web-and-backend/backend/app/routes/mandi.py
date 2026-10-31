from fastapi import APIRouter, HTTPException, Query
from app.services.price_service import get_prices
from app.services.data_gov_client import DataGovAPIError

router = APIRouter(tags=["Mandi Prices"])


@router.get("/mandi-prices")
def mandi_prices(
    commodity: str = Query(..., min_length=1),
    state: str = Query(..., min_length=1),
    district: str | None = None,
    limit: int = Query(default=100, ge=1, le=1000),
):
    try:
        return get_prices(commodity, state, district, limit)
    except DataGovAPIError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
