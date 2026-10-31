from datetime import date, datetime
from typing import Any

from app.core.config import settings
from app.services.data_gov_client import fetch_mandi_records


def _number(value: Any) -> float | None:
    try:
        if value is None or str(value).strip() in {"", "-", "NA", "N/A"}:
            return None
        result = float(str(value).replace(",", "").strip())
        return result if result > 0 else None
    except (TypeError, ValueError):
        return None


def _parse_date(value: Any) -> date | None:
    if not value:
        return None
    text = str(value).strip()
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            pass
    return None


def normalize_record(raw: dict) -> dict | None:
    """Normalize one source row. Invalid/missing prices are rejected, not set to zero."""
    modal = _number(raw.get("modal_price"))
    minimum = _number(raw.get("min_price"))
    maximum = _number(raw.get("max_price"))
    arrival = _parse_date(raw.get("arrival_date"))

    required_text = ["state", "district", "market", "commodity"]
    if any(not str(raw.get(key, "")).strip() for key in required_text):
        return None
    if modal is None or arrival is None:
        return None
    if minimum is not None and maximum is not None and minimum > maximum:
        return None

    age_days = (date.today() - arrival).days
    return {
        "state": str(raw["state"]).strip(),
        "district": str(raw["district"]).strip(),
        "market": str(raw["market"]).strip(),
        "commodity": str(raw["commodity"]).strip(),
        "variety": str(raw.get("variety") or "").strip() or None,
        "grade": str(raw.get("grade") or "").strip() or None,
        "arrival_date": arrival.isoformat(),
        "min_price": minimum,
        "max_price": maximum,
        "modal_price": modal,
        "is_stale": age_days > settings.stale_after_days,
        "age_days": age_days,
        "source": "data.gov.in / AGMARKNET",
        "is_sample": False,
    }


def get_prices(commodity: str, state: str, district: str | None = None, limit: int = 100):
    payload = fetch_mandi_records(commodity, state, district, limit)
    normalized = []
    rejected = 0
    for raw in payload["records"]:
        item = normalize_record(raw)
        if item is None:
            rejected += 1
        else:
            normalized.append(item)

    # Keep the newest row for each market/variety/grade combination.
    newest = {}
    for item in normalized:
        key = (item["market"].casefold(), (item["variety"] or "").casefold(),
               (item["grade"] or "").casefold())
        if key not in newest or item["arrival_date"] > newest[key]["arrival_date"]:
            newest[key] = item

    results = sorted(newest.values(), key=lambda x: (x["modal_price"], x["market"]))
    return {
        "source": payload["source"],
        "resource_id": payload["resource_id"],
        "fetched_at": payload["fetched_at"],
        "total_source_records": payload["total"],
        "returned_records": len(results),
        "rejected_invalid_records": rejected,
        "records": results,
        "note": "Prices are reported wholesale modal prices, not guaranteed sale prices."
    }
