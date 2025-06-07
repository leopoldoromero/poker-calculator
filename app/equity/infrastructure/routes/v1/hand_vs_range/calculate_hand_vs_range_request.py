from typing import List
from pydantic import BaseModel, field_validator

class CalculateHandVsRangeEquityRequest(BaseModel):
    hero_hand: List[str]
    villain_range: List[str]
    board: List[str] = []

    @field_validator('hero_hand')
    def validate_cards(cls, v):
        if not all(len(card) == 2 for card in v):
            raise ValueError("All cards must be 2 characters long, example (KQs)")
        return v
    
    @field_validator('villain_range')
    def validate_range(cls, v):
        if not all(len(card) == 2 and len(card) <= 3 for card in v):
            raise ValueError("All range items must be between 2 or 3 characters long, example (KK+, AKo, JJ)")
        return v
    # >=