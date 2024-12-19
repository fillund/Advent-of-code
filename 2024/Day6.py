from aocd.models import Puzzle
import utils
from utils import Point
from enum import Enum, StrEnum, auto
from collections import Counter

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


def solve_a(data:str):
    grid = utils.parse_grid(data)
    guard_pos = [k for k,v in grid.items() if v == Symbol.GUARD][0]
    current_dir = Direction.UP
    grid[guard_pos] = Symbol.VISITIED
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
            break
        match grid[lookup]:
            case "#":
                current_dir = current_dir.turn()
            case "." | "X" | "^":
                grid[lookup] = Symbol.VISITIED.value
                guard_pos = lookup
            case _:
                raise ValueError

    counter = Counter(grid.values())
    print(counter)
    return counter[Symbol.VISITIED]

    
def solve_b(data:str):
    pass
                


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=6)

    example_a = solve_a(puzzle.example_data)
    assert (example_a == 41)
    answer_a = solve_a(puzzle.input_data)
    puzzle.answer_a = answer_a

    example_b = solve_b(puzzle.example_data)
    assert (example_b == 48)
    answer_b = solve_b(puzzle.input_data)
    puzzle.answer_b = answer_b
    