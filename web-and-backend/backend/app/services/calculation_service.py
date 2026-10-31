"""Business workflow for comparing mandi options."""

from app.models.schemas import CompareRequest
from app.services.calculations import compute_option, rank_options
from app.services.price_service import get_prices


def compare_mandis(request: CompareRequest) -> dict:
    """Fetch mandi prices, calculate estimated returns, and rank markets."""
    price_data = get_prices(
        commodity=request.commodity,
        state=request.state,
        district=request.district,
        limit=1000,
    )

    # Match expense entries to mandi names without case sensitivity.
    cost_by_market = {cost.market.strip().casefold(): cost for cost in request.costs}
    results = []

    for price in price_data["records"]:
        cost = cost_by_market.get(price["market"].strip().casefold())
        # Only compare markets for which the farmer supplied expenses.
        if cost is None:
            continue

        calculation = compute_option(
            modal_price_per_quintal=price["modal_price"],
            quantity_quintals=request.quantity_quintals,
            transport_cost=cost.transport_cost,
            other_expenses=cost.other_expenses,
        )

        results.append({
            "market": price["market"],
            "variety": price.get("variety"),
            "grade": price.get("grade"),
            "arrival_date": price["arrival_date"],
            "modal_price_per_quintal": price["modal_price"],
            "quantity_quintals": request.quantity_quintals,
            **calculation,
            "transport_cost": cost.transport_cost,
            "other_expenses": cost.other_expenses,
            "is_stale": price["is_stale"],
            "source": price["source"],
        })

    ranked_results = rank_options(results)

    return {
        "commodity": request.commodity,
        "state": request.state,
        "district": request.district,
        "quantity_quintals": request.quantity_quintals,
        "comparison_count": len(ranked_results),
        "best_market": ranked_results[0]["market"] if ranked_results else None,
        "results": ranked_results,
        "source": price_data["source"],
        "fetched_at": price_data["fetched_at"],
        "disclaimer": (
            "This is an estimate based on reported modal prices and expenses entered by the user. "
            "Actual sale price and other costs may differ. It is not a guaranteed profit."
        ),
        "message": (
            None if ranked_results else
            "No comparable mandi results found. Check crop/location spelling and submit expenses "
            "for market names returned by GET /api/v1/mandi-prices."
        ),
    }
