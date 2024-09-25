from aocd.models import Puzzle
import utils
from functools import reduce, total_ordering
from operator import mul, sub
from enum import IntEnum
from collections import Counter
import itertools as it
import math

CARDS = {'A':14, 'K':13, 'Q':12,'J':11, 'T':10}

def parse_hands(data:str):
    for line in data.splitlines():
        sHand, sBid = line.split(' ')
        hand = []
        for char in sHand:
            if char in CARDS:
                hand.append(CARDS[char])
            else:
                hand.append(int(char))
        bid = int(sBid)
        return hand, bid



        
if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=7)

    print(parse_hands(puzzle.example_data))
    # example_a = solve_a(puzzle.example_data)

