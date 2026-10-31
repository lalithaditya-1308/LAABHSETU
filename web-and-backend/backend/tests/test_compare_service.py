from datetime import datetime, timezone

from app.models.schemas import CompareRequest, MandiCostInput
from app.services import calculation_service


def test_compare_mandis_uses_calculations_and_ranks_by_net_return(monkeypatch):
    fake_price_data = {
        "records": [
            {
                "market": "Mandi A", "variety": "FAQ", "grade": None,
                "arrival_date": "2026-10-30", "modal_price": 2400,
                "is_stale": False, "source": "test source",
            },
            {
                "market": "Mandi B", "variety": "FAQ", "grade": None,
                "arrival_date": "2026-10-30", "modal_price": 2300,
                "is_stale": False, "source": "test source",
            },
        ],
        "source": "test source",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    }
    monkeypatch.setattr(calculation_service, "get_prices", lambda **kwargs: fake_price_data)

    request = CompareRequest(
        commodity="Wheat",
        state="Uttar Pradesh",
        quantity_quintals=20,
        costs=[
            MandiCostInput(market="Mandi A", transport_cost=3000, other_expenses=1000),
            MandiCostInput(market="Mandi B", transport_cost=1000, other_expenses=0),
        ],
    )

    result = calculation_service.compare_mandis(request)

    assert result["comparison_count"] == 2
    assert result["best_market"] == "Mandi B"
    assert result["results"][0]["estimated_net_return"] == 45000.00
    assert result["results"][1]["estimated_net_return"] == 44000.00
    assert result["results"][0]["gross_revenue"] == 46000.00
    assert "not a guaranteed profit" in result["disclaimer"]


def test_compare_mandis_matches_market_names_case_insensitively(monkeypatch):
    fake_price_data = {
        "records": [{
            "market": "Mandi A", "variety": None, "grade": None,
            "arrival_date": "2026-10-30", "modal_price": 1000,
            "is_stale": False, "source": "test source",
        }],
        "source": "test source",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    }
    monkeypatch.setattr(calculation_service, "get_prices", lambda **kwargs: fake_price_data)

    request = CompareRequest(
        commodity="Wheat",
        state="Uttar Pradesh",
        quantity_quintals=2,
        costs=[MandiCostInput(market="  mandi a  ", transport_cost=100)],
    )

    result = calculation_service.compare_mandis(request)
    assert result["comparison_count"] == 1
    assert result["best_market"] == "Mandi A"
    assert result["results"][0]["estimated_net_return"] == 1900.00


def test_compare_api_endpoint_returns_ranked_results(monkeypatch):
    from fastapi.testclient import TestClient
    from app.main import app

    fake_price_data = {
        "records": [{
            "market": "Mandi API", "variety": "FAQ", "grade": None,
            "arrival_date": "2026-10-30", "modal_price": 1500,
            "is_stale": False, "source": "test source",
        }],
        "source": "test source",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    }
    monkeypatch.setattr(calculation_service, "get_prices", lambda **kwargs: fake_price_data)

    client = TestClient(app)
    response = client.post(
        "/api/v1/compare",
        json={
            "commodity": "Wheat",
            "state": "Uttar Pradesh",
            "quantity_quintals": 10,
            "costs": [
                {"market": "Mandi API", "transport_cost": 500, "other_expenses": 250}
            ],
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["best_market"] == "Mandi API"
    assert body["results"][0]["gross_revenue"] == 15000.0
    assert body["results"][0]["total_expenses"] == 750.0
    assert body["results"][0]["estimated_net_return"] == 14250.0
