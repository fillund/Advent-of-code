from aocd.models import Puzzle
from typing import Tuple, Dict
from collections import defaultdict
from itertools import combinations, product, count
from functools import lru_cache, reduce
from operator import mul
import re

puzzle = Puzzle(year=2020, day=22)

sections = puzzle.input_data.split('\n\n')
player1 = [int(x) for x in sections[0].splitlines() if x.isnumeric()]
player2 = [int(x) for x in sections[1].splitlines() if x.isnumeric()]

def play_combat(deck1_:list, deck2_:list):
    deck1 = deck1_.copy()
    deck2 = deck2_.copy()
    while True:
        card1 = deck1.pop(0)
        card2 = deck2.pop(0)
        if card1 > card2:
            deck1.append(card1)
            deck1.append(card2)
        else:
            deck2.append(card2)
            deck2.append(card1)

        if len(deck1) == 0 or len(deck2) == 0:
            print(len(deck1), len(deck2))
            return deck1, deck2
        
deck1, deck2 = play_combat(player1, player2)
answer_a = sum((x*y for x,y in enumerate(reversed(deck1), start=1)))
print(answer_a)
puzzle.answer_a = answer_a


def recursive_combat(deck1_:list, deck2_:list):
    deck1 = deck1_.copy()
    deck2 = deck2_.copy()
    player1_history = set()
    player2_history = set()

    while True:
        if tuple(deck1) in player1_history and tuple(deck2) in player2_history:
            print('Default win!')
            return deck1, deck2
        player1_history.add(tuple(deck1))
        player2_history.add(tuple(deck2))
        card1 = deck1.pop(0)
        card2 = deck2.pop(0)
        if len(deck1) >= card1 and len(deck2) >= card2:
            p1, p2 = recursive_combat(deck1[:card1], deck2[:card2])
            if p1:
                deck1.append(card1)
                deck1.append(card2)
            else:
                deck2.append(card2)
                deck2.append(card1)
        elif card1 > card2:
            deck1.append(card1)
            deck1.append(card2)
        else:
            deck2.append(card2)
            deck2.append(card1)



        if len(deck1) == 0 or len(deck2) == 0:
            print(len(deck1), len(deck2))
            return deck1, deck2

d1, d2 = recursive_combat(player1, player2)
answer_b = sum((x*y for x,y in enumerate(reversed(d1), start=1)))
print(answer_b)
puzzle.answer_b = answer_b