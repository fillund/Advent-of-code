from aocd.models import Puzzle
import utils
from utils import Point
import more_itertools as mit


def is_accessible(grid:dict[Point, str], p:Point) -> bool:
    rolls = [n for n in utils.neighbours(p) if grid.get(n, '.')=='@']
    return len(rolls) < 4

def solve_a(data:str):
    grid = utils.parse_grid(data)
    rolls = [p for p in grid if grid[p] == '@']
    accessibles = [r for r in rolls if is_accessible(grid, r)]
    
    # print_grid = dict(grid)
    # print_grid.update({r:'x' for r in accessibles})
    # print(utils.grid_to_string(print_grid))
    return len(accessibles)

    
def solve_b(data:str):
    grid = utils.parse_grid(data)
    rolls = [p for p in grid if grid[p] == '@']
    grid = {k:v for k,v in grid.items() if v != '.'}
    accessibles = [r for r in rolls if is_accessible(grid, r)]
    removed = []
    while len(accessibles) > 0:
        for r in accessibles:
            grid[r] = '.'
            removed.append(r)
    
        rolls = [p for p in grid if grid[p] == '@']
        accessibles = [r for r in rolls if is_accessible(grid, r)]
    return len(removed)

                
example_data = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""

if __name__ == "__main__":
    puzzle = Puzzle(year=2025, day=4)

    example_a = solve_a(example_data)
    assert (example_a == 13)
    answer_a = solve_a(puzzle.input_data)
    puzzle.answer_a = answer_a

    example_b = solve_b(example_data)
    assert (example_b == 43)
    answer_b = solve_b(puzzle.input_data)
    puzzle.answer_b = answer_b
    