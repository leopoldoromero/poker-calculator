from pydantic import BaseModel

class CalculateEquityResponse(BaseModel):
    hero_equity: float
    villain_equity: float
    tie_equity: float
