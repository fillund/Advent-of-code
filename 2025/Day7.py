from aocd.models import Puzzle
import utils





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
    
    return 0


    
def solve_b(data:str):
    pass
                
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
    assert (example_b == 48)
    answer_b = solve_b(puzzle.input_data)
    puzzle.answer_b = answer_b
    