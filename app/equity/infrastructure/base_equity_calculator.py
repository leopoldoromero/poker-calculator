from typing import List, Literal
from treys import Card, Evaluator
import random

PocketPair = Literal[
    "22", "33", "44", "55", "66", "77", "88", "99",
    "TT", "JJ", "QQ", "KK", "AA"
]

class BaseEquityCalculator:
    def __init__(self, range_generator):
        self.range_generator = range_generator
        self.evaluator = Evaluator()
        self.pocket_pairs = (
            "22", "33", "44", "55", "66", "77", "88", "99",
            "TT", "JJ", "QQ", "KK", "AA"
        )
        self.PREBUILT_CARDS = {
            rank + suit: Card.new(rank + suit) for rank in "23456789TJQKA" for suit in "shdc"
        }

    def is_hand(self, hand: List[str]) -> bool:
        return len(hand) > 2 and all(len(card) > 2 for card in hand)

    def expand_range(self, range_: List[str]) -> List[str]:
        expanded = []
        for hand in range_:
            if "+" in hand and len(hand) == 3 and hand[0] == hand[1]:
                pair = hand[:2]
                if pair in self.pocket_pairs:
                    start_index = self.pocket_pairs.index(pair)
                    expanded.extend(self.pocket_pairs[start_index:])
            else:
                expanded.append(hand)
        return expanded

    def convert_card(self, card: str) -> int:
        return self.PREBUILT_CARDS[card]

    def convert_hand(self, hand: List[str]):
        """Converts a list of human-readable cards (e.g., ["As", "Kc"]) to Treys format."""
        return [self.convert_card(card) for card in hand]
    
    def simulate_matchup(self, hand1, hand2, board, num_simulations, deck):
        wins1, wins2, ties = 0, 0, 0
        num_to_draw = 5 - len(board)
        available_deck = [c for c in deck if c not in hand1 + hand2 + board]

        for _ in range(num_simulations):
            sampled_board = board + random.sample(available_deck, num_to_draw)
            score1 = self.evaluator.evaluate(sampled_board, hand1)
            score2 = self.evaluator.evaluate(sampled_board, hand2)

            if score1 < score2:
                wins1 += 1
            elif score2 < score1:
                wins2 += 1
            else:
                ties += 1

        return wins1, wins2, ties
