from aocd.models import Puzzle
import utils
from functools import cache




def solve_a(data:str):
    beams: list[list[int]] = [[]]
    splitters: list[list[int]] = []
    for line in data.splitlines():
        if not ("S" in line or "^" in line):
            continue
        if "S" in line:
            beams[0] = [line.find("S")]
        if "^" in line:
            splitters.append([i for i,c in enumerate(line) if c == "^"])
    
    num_split = 0
    for b_t, s_t in zip(beams, splitters):
        new_beams = set()
        for b in b_t:
            if b in s_t:
                new_beams.add(b-1)
                new_beams.add(b+1)
                num_split += 1
            else:
                new_beams.add(b)
        beams.append(list(new_beams))

    return num_split

@cache
def recurse_b(beam:int, remaining_splitters:tuple[tuple[int]]) -> int:
    if len(remaining_splitters) == 0:
        return 1

    for i,s in enumerate(remaining_splitters):
        if beam in s:
            remaining = remaining_splitters[i+1:] if len(remaining_splitters) > i else tuple()
            
            return recurse_b(beam-1, remaining_splitters=remaining) + recurse_b(beam+1, remaining_splitters=remaining)
    else:
        return 1

    
def solve_b(data:str):
    beams: list[list[int]] = [[]]
    splitters: list[tuple[int]] = []
    for line in data.splitlines():
        if not ("S" in line or "^" in line):
            continue
        if "S" in line:
            beams[0] = [line.find("S")]
        if "^" in line:
            pos = [i for i,c in enumerate(line) if c == "^"]
            splitters.append(tuple(pos))  # type: ignore

    timelines = recurse_b(beams[0][0], tuple(splitters))
    return timelines
                
example_data = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""

if __name__ == "__main__":
    puzzle = Puzzle(year=2025, day=7)

    example_a = solve_a(example_data)
    assert (example_a == 21)
    answer_a = solve_a(puzzle.input_data)
    puzzle.answer_a = answer_a

    example_b = solve_b(example_data)
    assert (example_b == 40)
    answer_b = solve_b(puzzle.input_data)
    puzzle.answer_b = answer_b
    