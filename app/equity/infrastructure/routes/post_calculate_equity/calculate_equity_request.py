from pydantic import BaseModel

class CalculateEquityRequest(BaseModel):
    hand: list
    range: list 
    board: list = []