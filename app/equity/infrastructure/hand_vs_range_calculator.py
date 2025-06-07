import random
from treys import Card
from app.equity.infrastructure.hands_from_range_generator import HandsFromRangeGenerator
from app.equity.domain.equity_calculator import EquityCalculator
from app.equity.infrastructure.base_equity_calculator import BaseEquityCalculator
from typing import Literal

PocketPair = Literal[
    "22", "33", "44", "55", "66", "77", "88", "99",
    "TT", "JJ", "QQ", "KK", "AA"
]

PREBUILT_CARDS = {
    rank + suit: Card.new(rank + suit) for rank in "23456789TJQKA" for suit in "shdc"
}

class HandVsRangeEquityCalculator(BaseEquityCalculator, EquityCalculator):
    def __init__(self, range_generator: HandsFromRangeGenerator):
        super().__init__(range_generator)
        # self.range_generator = range_generator
        # self.evaluator = Evaluator()


    # def convert_card(self, card: str):
    #     """Converts a human-readable card format (e.g., "As") to Treys format."""
    #     # rank_map = {
    #     #     "2": "2",
    #     #     "3": "3",
    #     #     "4": "4",
    #     #     "5": "5",
    #     #     "6": "6",
    #     #     "7": "7",
    #     #     "8": "8",
    #     #     "9": "9",
    #     #     "T": "T",
    #     #     "J": "J",
    #     #     "Q": "Q",
    #     #     "K": "K",
    #     #     "A": "A",
    #     # }
    #     # suit_map = {'♠': 's', '♥': 'h', '♦': 'd', '♣': 'c'}
    #     # suit_map = {"s": "s", "h": "h", "d": "d", "c": "c"}
    #     # return Card.new(rank_map[card[0]] + suit_map[card[1]])
    #     return PREBUILT_CARDS[card]

    # def convert_hand(self, hand: List[str]):
    #     """Converts a list of human-readable cards (e.g., ["As", "Kc"]) to Treys format."""
    #     return [self.convert_card(card) for card in hand]

    # def expand_range(self, opponent_range: List[str]) -> List[str]:
    #     """Expands shorthand range notation like 'JJ+' to explicit hand representations."""
    #     expanded_range = []
    #     # pocket_pairs = "22 33 44 55 66 77 88 99 TT JJ QQ KK AA".split()
    #     pocket_pairs: Tuple[PocketPair, ...] = (
    #         "22", "33", "44", "55", "66", "77", "88", "99",
    #         "TT", "JJ", "QQ", "KK", "AA"
    #     )

    #     for hand in opponent_range:
    #         if (
    #             "+" in hand and len(hand) == 3 and hand[0] == hand[1]
    #         ):  # Detect pocket pair shorthand like "JJ+"
    #             pair = hand[:2]
    #             if pair in pocket_pairs:
    #                 start_index = pocket_pairs.index(hand[:2])
    #                 expanded_range.extend(pocket_pairs[start_index:])
    #         else:
    #             expanded_range.append(hand)  # Keep suited/offsuit hands as they are

    #     return expanded_range

    # def simulate_matchup(self, hand1: List[int], hand2: List[int], board: List[int], num_simulations: int, deck: List[int]):
    #     """
    #     Simulates matchups between hand1 and hand2 using Monte Carlo, avoiding duplicate cards.
    #     :param hand1: List of int like [546233, 2343233] representing a player hand in treys format.
    #     :param hand2: List of int like [546233, 2343233] representing a player hand in treys format.
    #     :param board: List of int like [546233, 2343233] representing board hadns in treys format.
    #     :param num_simulations: int that indicates the number of simulations to run.
    #     :param deck List of int like [546233, 2343233, 435443] representing the available cards in the deck in treys format.
    #     """
    #     wins_hand1, wins_hand2, ties = 0, 0, 0
    #     num_cards_to_deal = 5 - len(board)

    #     # Ensure drawn cards do not include duplicates
    #     available_deck = [
    #         card
    #         for card in deck
    #         if card not in hand1 and card not in hand2 and card not in board
    #     ]

    #     if len(available_deck) < num_cards_to_deal:
    #         raise ValueError(
    #             f"Not enough cards to deal. Available deck size: {len(available_deck)}, Needed: {num_cards_to_deal}"
    #         )

    #     for _ in range(num_simulations):
    #         new_board = board + random.sample(available_deck, 5 - len(board))

    #         if len(new_board) != 5 or len(hand1) != 2 or len(hand2) != 2:
    #             raise ValueError(
    #                 f"Invalid number of cards: board={len(new_board)}, hand1={len(hand1)}, hand2={len(hand2)}"
    #             )

    #         try:
    #             score1 = self.evaluator.evaluate(new_board, hand1)
    #             score2 = self.evaluator.evaluate(new_board, hand2)
    #         except KeyError as e:
    #             print(f"KeyError: {e}")
    #             raise
    #         except TypeError as e:
    #             print(f"TypeError: {e}")
    #             raise

    #         if score1 < score2:
    #             wins_hand1 += 1
    #         elif score2 < score1:
    #             wins_hand2 += 1
    #         else:
    #             ties += 1

    #     return wins_hand1, wins_hand2, ties

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

        expanded_range = self.expand_range(villain_cards_or_range)
        # Generate deck without known cards
        deck = [Card.new(rank + suit) for rank in "23456789TJQKA" for suit in "shdc"]
        deck = [card for card in deck if card not in hero_cards_or_range + board]

        # Generate all possible opponent hands
        opponent_hands = self.range_generator.generate(
            expanded_range, excluded_cards=hero_cards_or_range + board[:]
        )
        MAX_OPPONENT_HANDS = 150
        opponent_hands = [self.convert_hand(hand) for hand in opponent_hands]
        opponent_hands = random.sample(
            opponent_hands, min(len(opponent_hands), MAX_OPPONENT_HANDS)
        )

        total_wins1, total_wins2, total_ties = 0, 0, 0
        num_hands = len(opponent_hands)
        hero_cards_or_range = self.convert_hand(hero_cards_or_range)
        board = self.convert_hand(board)

        for opp_hand in opponent_hands:
            deck_copy = [
                card for card in deck if card not in opp_hand
            ]  # Exclude opponent's hand from deck

            wins1, wins2, ties = self.simulate_matchup(
                hero_cards_or_range, opp_hand, board, num_simulations, deck_copy
            )

            total_wins1 += wins1
            total_wins2 += wins2
            total_ties += ties
        if num_simulations * num_hands == 0:
            raise ValueError(
                f"No hands to simulate, SIMS: {num_simulations}, HANDS: {num_hands}"
            )
        total_sims = num_simulations * num_hands
        equity_hand1 = (total_wins1) / total_sims
        equity_range = (total_wins2) / total_sims
        tie_percentage = total_ties / total_sims

        return equity_hand1, equity_range, tie_percentage
