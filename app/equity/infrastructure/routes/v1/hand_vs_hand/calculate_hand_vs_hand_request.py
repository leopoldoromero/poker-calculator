from typing import List
from pydantic import BaseModel, field_validator

class CalculateHandVsHandEquityRequest(BaseModel):
    hero_hand: List[str]
    villain_hand: List[str]
    board: List[str] = []

    @field_validator('hero_hand', 'villain_hand')
    def validate_cards(cls, v):
        if not all(len(card) == 2 for card in v):
            raise ValueError("All cards must be 2 characters long, example (KQs)")
        return v
