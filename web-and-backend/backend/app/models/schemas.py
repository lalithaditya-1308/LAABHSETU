from typing import Optional
from pydantic import BaseModel, Field, field_validator


class MandiCostInput(BaseModel):
    market: str = Field(min_length=1, description="Exact mandi/market name from the price results")
    transport_cost: float = Field(default=0, ge=0)
    other_expenses: float = Field(default=0, ge=0)


class CompareRequest(BaseModel):
    commodity: str = Field(min_length=1)
    state: str = Field(min_length=1)
    district: Optional[str] = None
    quantity_quintals: float = Field(gt=0)
    costs: list[MandiCostInput] = Field(min_length=1)

    @field_validator("commodity", "state")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be blank")
        return value


class NetReturnResult(BaseModel):
    market: str
    variety: Optional[str] = None
    grade: Optional[str] = None
    arrival_date: str
    modal_price_per_quintal: float
    quantity_quintals: float
    gross_revenue: float
    transport_cost: float
    other_expenses: float
    total_expenses: float
    estimated_net_return: float
    is_stale: bool
    source: str
