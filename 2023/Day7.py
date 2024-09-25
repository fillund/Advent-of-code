from aocd.models import Puzzle
import utils
from functools import reduce, total_ordering
from operator import mul
from enum import IntEnum
from collections import Counter
import itertools as it


card2num = {'A':14, 'K':13, 'Q':12, 'J':11, 'T':10}

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
    def __init__(self, line:str) -> None:
        hand_str, bid_str = line.split()
        cards = [card2num.get(c, c) for c in hand_str]
        self.cards = list(map(int, cards))
        self.bid = int(bid_str)
        self.check_type()

    def check_type(self):
        card_count = Counter(self.cards)
        if len(card_count) == 1:
            self.type_ = HandType.FIVE_OF_A_KIND
        if max(card_count.values()) == 4:
            self.type_ = HandType.FOUR_OF_A_KIND
        elif max(card_count.values()) == 3 and len(card_count) == 2:
            self.type_ = HandType.FULL_HOUSE
        elif max(card_count.values()) == 2 and len(card_count) == 3:
            self.type_ = HandType.TWO_PAIR
        elif max(card_count.values()) == 3:
            self.type_ = HandType.THREE_OF_A_KIND # Can not be full house, already checked above
        elif max(card_count.values()) == 2:
            self.type_ = HandType.ONE_PAIR # Can not be two pair, handled above
        else:
            self.type_ = HandType.HIGH_CARD
        
    def __lt__(self, other:'Hand'):
        if self.type_ < other.type_:
            return True
        elif self.type_ > other.type_:
            return False
        for (mine, others) in zip(self.cards, other.cards):
            if mine < others:
                return True
            elif mine > others:
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

    return 0

if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=7)

    example_a = solve_a(puzzle.example_data)
    assert (example_a == 6440)
    puzzle.answer_a = solve_a(puzzle.input_data)

    # example_b = solve_b(puzzle.example_data)
    # assert(example_b == 71503)
    # puzzle.answer_b = solve_b(puzzle.input_data)