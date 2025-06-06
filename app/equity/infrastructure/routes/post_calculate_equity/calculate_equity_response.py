from pydantic import BaseModel

class CalculateEquityResponse(BaseModel):
    hand_equity: float
    range_equity: float
    tie_equity: float
