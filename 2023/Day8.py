from aocd.models import Puzzle
import utils
from functools import reduce, total_ordering
from operator import mul
from enum import IntEnum
from collections import Counter
import itertools as it
import math


def parse_data(data:str) -> tuple[str, dict[str, tuple[str, str]]]:
    line_iter = iter(data.splitlines())
    instruction = next(line_iter).strip()
    network: dict[str, tuple[str, str]] = {}
    next(line_iter) # Skip empty line
    for line in line_iter:
        start, targets = line.split(' = ')
        l, r = targets.strip('() ').split(', ')
        network[start] = (l.strip(), r.strip())
    return instruction, network

def solve_a(data:str) -> int:
    instructions, network = parse_data(data)
    current = 'AAA'
    for i, dir in enumerate(it.cycle(instructions), start=1):
        if dir == 'L':
            current = network[current][0]
        else:
            current = network[current][1]
        if current == 'ZZZ':
            return i

def find_starts(network: dict[str, tuple]):
    return [a for a in network.keys() if a.endswith('A')]

def solve_b(data:str) -> int:
    instructions, network = parse_data(data)

    current = find_starts(network)
    print(f'There are {len(current)} ghosts')
    first_z = {}
    for i, dir in enumerate(it.cycle(instructions), start=1):
        target = []
        for node in current:
            if dir == 'L':
                target.append(network[node][0])
            else:
                target.append(network[node][1])
        current = target
        for num, node in enumerate(current):
            if node.endswith('Z'):
                first_z[num] = i
                print(f'Ghost {num} hits a Z node at {i}')
        if all([a.endswith('Z') for a in current]):
            return i
        if len(first_z) == len(current):
            return math.lcm(*first_z.values())

    

if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=8)

    example_a = solve_a(puzzle.example_data)
    assert (example_a == 2)
    puzzle.answer_a = solve_a(puzzle.input_data)

    example_data = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

    example_b = solve_b(example_data)
    assert(example_b == 6)
    puzzle.answer_b = solve_b(puzzle.input_data)