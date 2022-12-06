from aocd.models import Puzzle
from collections.abc import Sequence
import itertools as it

puzzle = Puzzle(2022, 6)

def nwise(iterable:Sequence, n:int)->Sequence[tuple]:
    iters = it.tee(iterable, n)
    for i, iterator in enumerate(iters):
        for _ in range(i):
            next(iterator, None)
    return zip (*iters)
    

def find_start_marker(stream:str, n:int)->int:
    for i, quad in enumerate(nwise(stream, n), start=n):
        if len(set(quad)) == n:
            return i

assert(find_start_marker(puzzle.example_data, 4) == 7)

puzzle.answer_a = find_start_marker(puzzle.input_data, 4)
puzzle.answer_b = find_start_marker(puzzle.input_data, 14)