from aocd.models import Puzzle
from typing import Tuple, Dict
from collections import defaultdict
from itertools import combinations, product, count
from functools import lru_cache, reduce
from operator import mul
import re

puzzle = Puzzle(year=2020, day=25)

public_keys = [int(x) for x in puzzle.input_data.splitlines()]

def transform(subject_number:int, loop_size:int) -> int:
    value = 1
    for i in range(loop_size):
        value *= subject_number
        value %= 20201227 # magic number
    return value

def find_loop(target:int) -> int:
    value = 1
    subject_number = 7
    for i in count(1):
        value *= subject_number
        value %= 20201227 # magic number
        if value == target:
            break
    return i

answer_a = transform(public_keys[1], find_loop(public_keys[0]))
print(answer_a)
puzzle.answer_a = answer_a