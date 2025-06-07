import random
from treys import Card
from app.equity.infrastructure.hands_from_range_generator import HandsFromRangeGenerator
from app.equity.domain.equity_calculator import EquityCalculator
from app.equity.infrastructure.base_equity_calculator import BaseEquityCalculator
from typing import Literal, List

PocketPair = Literal[
    "22", "33", "44", "55", "66", "77", "88", "99",
    "TT", "JJ", "QQ", "KK", "AA"
]

PREBUILT_CARDS = {
    rank + suit: Card.new(rank + suit) for rank in "23456789TJQKA" for suit in "shdc"
}

class RangeVsRangeEquityCalculator(BaseEquityCalculator, EquityCalculator):
    def __init__(self, range_generator: HandsFromRangeGenerator):
        super().__init__(range_generator)

    def trasnform_range_card_in_card(self, range_card: str):
        rank1, rank2 = range_card[:2]
        simbol = range_card[2] if len(range_card) > 2 else None
        suits = "schd"
        
        if simbol is None:
            return [
                [rank1 + s1, rank2 + s2]
                for i, s1 in enumerate(suits)
                for j, s2 in enumerate(suits)
                if i < j ]
        if simbol == "+" and rank1 == rank2:
            pair = rank1 + rank2
            start_idx = self.pocket_pairs.index(pair)
            expanded_pairs = self.pocket_pairs[start_idx:]
            return [
                [rank[0] + s1, rank[1] + s2]
                for rank in expanded_pairs
                for i, s1 in enumerate(suits)
                for j, s2 in enumerate(suits)
                if i < j  
            ]
        cards_by_simbol = {
                "o": [
                [rank1 + suit1, rank2 + suit2]
                for suit1 in suits
                for suit2 in suits
                if suit1 != suit2
                ],
                "s": [[rank1 + suit, rank2 + suit] for suit in suits],
            }
        return cards_by_simbol[simbol]

    def execute(self, hero_cards_or_range, villain_cards_or_range, board=[], num_simulations=500):
        """
        Runs a Monte Carlo simulation of a hand vs an opponent's range.
        :param hero_cards_or_range List of str representing a player hand (e.g., ["Qs", "Kh"])
        :param villain_cards_or_range List of str representing a player range (e.g., ["JJ", "AQs", "AQo", "KQs"])
        :param board List of str representing the cards of the board (e.g., ["As", "Ks", "Js", "Th", "3d"]),
        optional default [].
        :param num_simulations int Indicates the number of simulations to run.
        optional default 10000
        :returns tuple[float, float, float] with the values that represents the equity of hero_cards_or_range, equity of range,
        equity of tie (e.g [28.02, 62.11, 9.87])
        """

        expanded_hero_range = self.expand_range(hero_cards_or_range)
        expanded_villain_range = self.expand_range(villain_cards_or_range)
        hero_transformed_range = [self.trasnform_range_card_in_card(range_item) for range_item in hero_cards_or_range]
        villain_transformed_range = [self.trasnform_range_card_in_card(range_item) for range_item in villain_cards_or_range]

        print(f"CHECK1: {expanded_villain_range}")
        deck = [Card.new(rank + suit) for rank in "23456789TJQKA" for suit in "shdc"]
        deck = [card for card in deck if card not in hero_transformed_range + board]

        # Generate all possible opponent hands
        hero_hands = self.range_generator.generate(
            expanded_hero_range, excluded_cards=villain_transformed_range + board[:]
        )
        villain_hands = self.range_generator.generate(
            expanded_villain_range, excluded_cards=hero_transformed_range + board[:]
        )
        print(f"CHECK2: {hero_hands}")
        MAX_OPPONENT_HANDS = 150
        hero_hands = [self.convert_hand(hand) for hand in hero_hands]
        hero_hands = random.sample(
            hero_hands, min(len(hero_hands), MAX_OPPONENT_HANDS)
        )

        villain_hands = [self.convert_hand(hand) for hand in villain_hands]
        villain_hands = random.sample(
            villain_hands, min(len(villain_hands), MAX_OPPONENT_HANDS)
        )

        total_wins1, total_wins2, total_ties = 0, 0, 0
        num_hands = len(villain_hands)
        # hero_cards_or_range = self.convert_hand(hero_cards_or_range)
        board = self.convert_hand(board)

        for hero_hand in hero_hands:
            for villain_hand in villain_hands:
                deck_copy = [
                    card for card in deck
                    if card not in hero_hand and card not in villain_hand
                ]

                wins1, wins2, ties = self.simulate_matchup(
                    hero_hand, villain_hand, board, num_simulations, deck_copy
                )

                total_wins1 += wins1
                total_wins2 += wins2
                total_ties += ties

        if num_simulations * num_hands == 0:
            raise ValueError(
                f"No hands to simulate, SIMS: {num_simulations}, HANDS: {num_hands}"
            )
        total_sims = num_simulations * len(hero_hands) * len(villain_hands)
        equity_hand1 = (total_wins1) / total_sims
        equity_range = (total_wins2) / total_sims
        tie_percentage = total_ties / total_sims

        return equity_hand1, equity_range, tie_percentage
