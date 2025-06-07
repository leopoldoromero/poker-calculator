from app.equity.infrastructure.hands_from_range_generator import HandsFromRangeGenerator
from app.equity.infrastructure.hand_vs_range_calculator import HandVsRangeEquityCalculator
from app.equity.infrastructure.hand_vs_hand_calculator import HandVsHandEquityCalculator
from app.equity.infrastructure.range_vs_range_calculator import RangeVsRangeEquityCalculator

range_generator = HandsFromRangeGenerator()
hand_vs_range_equity_calculator = HandVsRangeEquityCalculator(range_generator)
hand_vs_hand_equity_calculator = HandVsHandEquityCalculator(range_generator)
range_vs_range_equity_calculator = RangeVsRangeEquityCalculator(range_generator)

d_container = {
    "hand_vs_range_equity_calculator": hand_vs_range_equity_calculator,
    "hand_vs_hand_equity_calculator": hand_vs_hand_equity_calculator,
    "range_vs_range_equity_calculator": range_vs_range_equity_calculator,
}


def get_dependency(name: str):
    if name not in d_container:
        raise Exception(f"Dependency {name} does not exist in the container")
    return d_container[name]
