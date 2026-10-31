from datetime import datetime, timezone
import requests

from app.core.config import settings


class DataGovAPIError(RuntimeError):
    """Raised when data.gov.in cannot provide a usable response."""


def fetch_mandi_records(
    commodity: str,
    state: str,
    district: str | None = None,
    limit: int | None = None,
) -> dict:
    """
    Fetch daily mandi prices from the official data.gov.in resource generated
    through AGMARKNET. Filters are applied by data.gov.in before records return.
    """
    if not settings.data_gov_api_key:
        raise DataGovAPIError(
            "DATA_GOV_API_KEY is not configured. Add your key to backend/.env."
        )

    url = f"{settings.data_gov_base_url.rstrip('/')}/{settings.data_gov_resource_id}"
    params = {
        "api-key": settings.data_gov_api_key,
        "format": "json",
        "limit": min(limit or settings.api_page_size, settings.api_page_size),
        "offset": 0,
        "filters[commodity]": commodity,
        # The resource exposes state as a keyword field on the data.gov.in API.
        "filters[state.keyword]": state,
    }
    if district:
        params["filters[district]"] = district

    try:
        response = requests.get(url, params=params, timeout=settings.api_timeout_seconds)
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        raise DataGovAPIError(f"Could not reach data.gov.in: {exc}") from exc
    except ValueError as exc:
        raise DataGovAPIError("data.gov.in returned a response that was not valid JSON.") from exc

    if not isinstance(payload, dict):
        raise DataGovAPIError("Unexpected data.gov.in response format.")

    records = payload.get("records")
    if not isinstance(records, list):
        message = payload.get("message", "No records field was returned.")
        raise DataGovAPIError(f"data.gov.in response did not contain records: {message}")

    return {
        "records": records,
        "total": payload.get("total", len(records)),
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "source": "data.gov.in / AGMARKNET",
        "resource_id": settings.data_gov_resource_id,
    }
