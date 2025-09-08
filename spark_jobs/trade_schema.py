from __future__ import annotations
from pydantic import BaseModel, Field, field_validator
from typing import Literal, Optional
from datetime import datetime

Side = Literal["BUY", "SELL"]

class Trade(BaseModel):
    trade_id: str
    ts_event: datetime
    symbol: str
    side: Side
    price: float = Field(gt=0)
    quantity: int = Field(gt=0)
    venue: str
    trader_id: Optional[str] = None

    @field_validator("symbol")
    @classmethod
    def upper_symbol(cls, v: str) -> str:
        return v.upper()

    def to_json(self) -> str:
        # Serialize with ISO timestamp
        return self.model_dump_json()