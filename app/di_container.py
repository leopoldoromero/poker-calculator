from app.equity.infrastructure.hands_from_range_generator import HandsFromRangeGenerator
from app.equity.infrastructure.hand_vs_range_calculator import HandVsRangeEquityCalculator

range_generator = HandsFromRangeGenerator()
equity_calculator = HandVsRangeEquityCalculator(range_generator)

d_container = {
    "equity_calculator": equity_calculator,
}


def get_dependency(name: str):
    if name not in d_container:
        raise Exception(f"Dependency {name} does not exist in the container")
    return d_container[name]
