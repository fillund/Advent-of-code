from aocd.models import Puzzle
import utils
from utils import Point
from enum import Enum, StrEnum, auto
from collections import Counter
from typing import Sequence, Iterable
from tqdm import tqdm

class Direction(Enum):
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()

    def turn(self):
        match self:
            case Direction.UP:
                return Direction.RIGHT
            case Direction.RIGHT:
                return Direction.DOWN
            case Direction.DOWN:
                return Direction.LEFT
            case Direction.LEFT:
                return Direction.UP

class Symbol(StrEnum):
    GUARD = "^"
    OBSTACLE = "#"
    VISITIED = "X"
    EMPTY = "."

def make_path(grid) -> tuple[dict[Point, None], bool]:
    grid = grid.copy()
    guard_pos = [k for k,v in grid.items() if v == Symbol.GUARD][0]
    current_dir = Direction.UP
    grid[guard_pos] = Symbol.VISITIED
    path = {guard_pos:None}
    is_loop = False
    bumped_obstacles: set[tuple[Point, Direction]] = set()
    while guard_pos in grid:
        match current_dir:
            case Direction.UP:
                lookup = Point(guard_pos.x, guard_pos.y-1)
            case Direction.RIGHT:
                lookup = Point(guard_pos.x+1, guard_pos.y)
            case Direction.DOWN:
                lookup = Point(guard_pos.x, guard_pos.y+1)
            case Direction.LEFT:
                lookup = Point(guard_pos.x-1, guard_pos.y)
        
        if lookup not in grid:
            is_loop = False
            break
        match grid[lookup]:
            case "#":
                if (lookup, current_dir) in bumped_obstacles:
                    is_loop = True
                    break
                bumped_obstacles.add((lookup, current_dir))
                current_dir = current_dir.turn()

            case "." | "X" | "^":
                grid[lookup] = Symbol.VISITIED.value
                guard_pos = lookup
                path[lookup] = None
            case _:
                raise ValueError
    return path, is_loop
    

def solve_a(data:str):
    grid = utils.parse_grid(data)
    path,_ = make_path(grid)

    return len(path)

    
def solve_b(data:str):
    grid = utils.parse_grid(data)
    guard_pos = [k for k,v in grid.items() if v == Symbol.GUARD][0]
    path, _ = make_path(grid)
    del path[guard_pos]
    loops = 0
    for p in tqdm(path):
        new_grid = grid.copy()
        new_grid[p] = Symbol.OBSTACLE.value
        _, is_loop = make_path(new_grid)
        if is_loop:
            loops+=1
    return loops

                


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=6)

    example_a = solve_a(puzzle.example_data)
    assert (example_a == 41)
    answer_a = solve_a(puzzle.input_data)
    puzzle.answer_a = answer_a

    example_b = solve_b(puzzle.example_data)
    assert (example_b == 6)
    answer_b = solve_b(puzzle.input_data)
    puzzle.answer_b = answer_b
    