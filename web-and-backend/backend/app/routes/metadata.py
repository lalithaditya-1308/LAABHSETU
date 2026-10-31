from fastapi import APIRouter

router = APIRouter(tags=["Metadata"])


@router.get("/crops")
def crops():
    return {
        "items": ["Wheat", "Rice", "Potato", "Onion"],
        "note": "Starter list for the MVP. Replace/extend using verified dataset values."
    }


@router.get("/locations")
def locations():
    return {
        "items": [],
        "note": "Location options should be populated from verified mandi records."
    }
