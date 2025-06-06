from abc import ABC, abstractmethod
from typing import List, Tuple


class EquityCalculator(ABC):
    @abstractmethod
    def execute(self, hand1: List[str], opponent_range: List[str], board:  List[str] = [], num_simulations: int = 500) -> Tuple[float, float, float]:
        pass