"""Deterministic financial calculations for mandi comparisons."""

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Any


_CENT = Decimal("0.01")


def _as_decimal(value: Any, field_name: str) -> Decimal:
    """Convert an input to a finite Decimal without using binary float math."""
    try:
        result = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError(f"{field_name} must be a valid number.") from None

    if not result.is_finite():
        raise ValueError(f"{field_name} must be a finite number.")
    return result


def _rounded_number(value: Decimal) -> float:
    """Round a Decimal to two places and return a plain Python number."""
    return float(value.quantize(_CENT, rounding=ROUND_HALF_UP))


def compute_option(
    modal_price_per_quintal: Any,
    quantity_quintals: Any,
    transport_cost: Any,
    other_expenses: Any,
) -> dict[str, float]:
    """Calculate gross revenue, total expenses, and estimated net return."""
    price = _as_decimal(modal_price_per_quintal, "modal_price_per_quintal")
    quantity = _as_decimal(quantity_quintals, "quantity_quintals")
    transport = _as_decimal(transport_cost, "transport_cost")
    expenses = _as_decimal(other_expenses, "other_expenses")

    if price <= 0:
        raise ValueError("modal_price_per_quintal must be greater than zero.")
    if quantity <= 0:
        raise ValueError("quantity_quintals must be greater than zero.")
    if transport < 0:
        raise ValueError("transport_cost must be zero or greater.")
    if expenses < 0:
        raise ValueError("other_expenses must be zero or greater.")

    gross_revenue = price * quantity
    total_expenses = transport + expenses
    estimated_net_return = gross_revenue - total_expenses

    return {
        "gross_revenue": _rounded_number(gross_revenue),
        "total_expenses": _rounded_number(total_expenses),
        "estimated_net_return": _rounded_number(estimated_net_return),
    }


def rank_options(options: list[dict]) -> list[dict]:
    """Sort options by net return descending, then transport cost ascending.

    Sorting is stable: if both ranking values tie, the input order is retained.
    The original list is not modified.
    """
    return sorted(
        options,
        key=lambda option: (
            -_as_decimal(option["estimated_net_return"], "estimated_net_return"),
            _as_decimal(option["transport_cost"], "transport_cost"),
        ),
    )
