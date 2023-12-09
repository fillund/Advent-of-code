from aocd.models import Puzzle
import utils
from functools import reduce
from operator import mul

def calc_distances(max_time) -> list[int]:
    return [(max_time-a)*a for a in range(max_time)]


def solve_a(data:str) -> int:
    times, distances = [utils.numbers(line) for line in data.splitlines()]
    ways_to_win = []
    for t,d in zip(times, distances):
        lengths = calc_distances(t)
        wins = [l > d for l in lengths]
        ways_to_win.append(sum(wins))
    
    return reduce(mul, ways_to_win)

def solve_b(data:str) -> int:
    times, distances = [utils.numbers(line) for line in data.splitlines()]
    t = int(''.join([str(a) for a in times]))
    d = int(''.join([str(a) for a in distances]))

    lengths = calc_distances(t)
    wins = [l > d for l in lengths]

    
    return sum(wins)

if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=6)

    example_a = solve_a(puzzle.example_data)
    assert (example_a == 288)
    puzzle.answer_a = solve_a(puzzle.input_data)

    example_b = solve_b(puzzle.example_data)
    assert(example_b == 71503)
    puzzle.answer_b = solve_b(puzzle.input_data)