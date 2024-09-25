from aocd.models import Puzzle
import utils
from functools import reduce, total_ordering
from operator import mul, sub
from enum import IntEnum
from collections import Counter
import itertools as it
import math

def running_diff(data: list[int]):
    # Diffs backwards rather than forwards
    return [b-a for a,b in it.pairwise(data)]

def recurse_diff(numbers: list[int], index=-1):
    diff = running_diff(numbers)
    if all([a == 0 for a in diff]):
        return diff[index]
    else:
        return diff[index] - recurse_diff(diff) * index

def solve_a(data:str, index=-1):
    lines = data.splitlines()
    values = []
    for line in lines:
        numbers = [int(a) for a in line.split(' ')]
        values.append(numbers[index] - recurse_diff(numbers, index)*index)
    return sum(values)


        
if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=9)

    example_a = solve_a(puzzle.example_data)

    assert(example_a == 114)
    answer_a = solve_a(puzzle.input_data)
    puzzle.answer_a = answer_a

    example_b = solve_a(puzzle.example_data, 1)

    assert(example_b == 2)

    puzzle.answer_b = solve_a(puzzle.input_data, 1)
