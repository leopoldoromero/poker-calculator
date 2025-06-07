from typing import List
from pydantic import BaseModel, field_validator

class CalculateRangeVsRangeEquityRequest(BaseModel):
    hero_range: List[str]
    villain_range: List[str]
    board: List[str] = []
    
    @field_validator('hero_range','villain_range')
    def validate_range(cls, v):
        if not all(len(card) >= 2 and len(card) <= 3 for card in v):
            raise ValueError("All range items must be between 2 or 3 characters long, example (KK+, AKo, JJ)")
        return v