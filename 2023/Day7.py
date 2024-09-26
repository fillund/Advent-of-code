from aocd.models import Puzzle
import utils
from functools import reduce, total_ordering
from operator import mul
from enum import IntEnum
from collections import Counter
import itertools as it


CARDS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

class HandType(IntEnum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7

@total_ordering
class Hand:
    def __init__(self, line:str, transform_jokers = False) -> None:
        self.all_cards = CARDS
        if transform_jokers:
            self.all_cards.remove('J')
            self.all_cards.append('J')
        hand_str, bid_str = line.split()
        self.cards = hand_str
        self.bid = int(bid_str)
        if transform_jokers:
            self.type_ = self.check_type(self.transform_cards(self.cards))
        else:
            self.type_ = self.check_type(self.cards)

    def transform_cards(self, cards:str):
        card_count = Counter(cards)
        if 'J' in card_count:
            card_count['J'] = 0
        cards = cards.replace('J', card_count.most_common(1)[0][0])
        return cards


    def check_type(self, cards):
        card_count = Counter(cards)
        if len(card_count) == 1:
            return HandType.FIVE_OF_A_KIND
        elif max(card_count.values()) == 4:
            return HandType.FOUR_OF_A_KIND
        elif max(card_count.values()) == 3 and len(card_count) == 2:
            return HandType.FULL_HOUSE
        elif max(card_count.values()) == 2 and len(card_count) == 3:
            return HandType.TWO_PAIR
        elif max(card_count.values()) == 3:
            return HandType.THREE_OF_A_KIND # Can not be full house, already checked above
        elif max(card_count.values()) == 2:
            return HandType.ONE_PAIR # Can not be two pair, handled above
        else:
            return HandType.HIGH_CARD
        
    def __lt__(self, other:'Hand'):
        if self.type_ < other.type_:
            return True
        elif self.type_ > other.type_:
            return False
        for (mine, others) in zip(self.cards, other.cards):
            if self.all_cards.index(mine) > self.all_cards.index(others):
                return True
            elif self.all_cards.index(mine) < self.all_cards.index(others):
                return False
        raise ValueError # Can not be equal

    def __repr__(self) -> str:
        return f'{self.type_} - {self.cards}'

def solve_a(data:str) -> int:
    hands = [Hand(line) for line in data.splitlines()]
    sorted_hands = sorted(hands)
    winnings = [h.bid*i for (i, h) in enumerate(sorted_hands, start=1)]
    return sum(winnings)

def solve_b(data:str) -> int:
    hands = [Hand(line, transform_jokers=True) for line in data.splitlines()]
    sorted_hands = sorted(hands)
    winnings = [h.bid*i for (i, h) in enumerate(sorted_hands, start=1)]
    return sum(winnings)


REDDIT_CASE = """AAAAA 2
22222 3
AAAAK 5
22223 7
AAAKK 11
22233 13
AAAKQ 17
22234 19
AAKKQ 23
22334 29
AAKQJ 31
22345 37
AKQJT 41
23456 43"""

if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=7)

    example_a = solve_a(puzzle.example_data)
    example_reddit = solve_a(REDDIT_CASE)
    assert (example_a == 6440)
    assert(example_reddit == 1343)
    puzzle.answer_a = solve_a(puzzle.input_data)

    example_b = solve_b(puzzle.example_data)
    assert(example_b == 5905)
    assert(solve_b(REDDIT_CASE) == 1369)
    puzzle.answer_b = solve_b(puzzle.input_data)