from abc import ABC, abstractmethod
from typing import List, Tuple


class EquityCalculator(ABC):
    @abstractmethod
    def execute(self, hero_cards_or_range: List[str], villain_cards_or_range: List[str], board:  List[str] = [], num_simulations: int = 500) -> Tuple[float, float, float]:
        pass