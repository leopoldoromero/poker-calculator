import random
from treys import Card
from app.equity.domain.equity_calculator import EquityCalculator
from app.equity.infrastructure.base_equity_calculator import BaseEquityCalculator
from app.equity.infrastructure.hands_from_range_generator import HandsFromRangeGenerator

class HandVsHandEquityCalculator(BaseEquityCalculator, EquityCalculator):
    def __init__(self, range_generator: HandsFromRangeGenerator):
        super().__init__(range_generator)

    def execute(self, hero_cards_or_range, villain_cards_or_range, board=[], num_simulations=1000):
        deck = [Card.new(rank + suit) for rank in "23456789TJQKA" for suit in "shdc"]
        hand1 = self.convert_hand(hero_cards_or_range)
        hand2 = self.convert_hand(villain_cards_or_range)

        for card in hand1 + hand2:
            deck.remove(card)

        wins_hand1 = 0
        wins_hand2 = 0
        ties = 0

        for _ in range(num_simulations):
            board = random.sample(deck, 5)  
            score1 = self.evaluator.evaluate(board, hand1)
            score2 = self.evaluator.evaluate(board, hand2)

            if score1 < score2: 
                wins_hand1 += 1
            elif score2 < score1:
                wins_hand2 += 1
            else:
                ties += 1

        equity_hand1 = (wins_hand1 + ties / 2) / num_simulations
        equity_hand2 = (wins_hand2 + ties / 2) / num_simulations
        tie_percentage = ties / num_simulations

        return equity_hand1, equity_hand2, tie_percentage
