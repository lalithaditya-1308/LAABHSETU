import pytest

from app.services.calculations import compute_option, rank_options


def test_mandi_a_calculation():
    assert compute_option(2400, 20, 3000, 1000) == {
        "gross_revenue": 48000.00,
        "total_expenses": 4000.00,
        "estimated_net_return": 44000.00,
    }


def test_mandi_b_calculation():
    assert compute_option(2300, 20, 1000, 0) == {
        "gross_revenue": 46000.00,
        "total_expenses": 1000.00,
        "estimated_net_return": 45000.00,
    }


def test_zero_quantity_raises_value_error():
    with pytest.raises(ValueError, match="quantity_quintals"):
        compute_option(2400, 0, 3000, 1000)


def test_negative_transport_cost_raises_value_error():
    with pytest.raises(ValueError, match="transport_cost"):
        compute_option(2400, 20, -1, 1000)


def test_rank_options_by_net_return_then_transport_cost():
    options = [
        {"market": "Mandi A", "estimated_net_return": 44000, "transport_cost": 3000},
        {"market": "Mandi B", "estimated_net_return": 45000, "transport_cost": 1000},
        {"market": "Mandi C", "estimated_net_return": 45000, "transport_cost": 500},
    ]

    ranked = rank_options(options)

    assert [option["market"] for option in ranked] == [
        "Mandi C", "Mandi B", "Mandi A"
    ]
    # The helper returns a new list and does not mutate the input.
    assert [option["market"] for option in options] == [
        "Mandi A", "Mandi B", "Mandi C"
    ]
