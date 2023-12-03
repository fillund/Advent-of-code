from aocd.models import Puzzle
from utils import Point, neighbours
import re

class Partgrid:

    NUM_PATTERN = re.compile(r'\d+')
    SYMBOL_PATTERN = re.compile(r'[^.0-9]')

    def __init__(self) -> None:
        self.symbol_grid: dict[Point, str] = {}
        self.number_grid: dict[Point, int] = {}

    def numbers_from_str(self, data:str):
        for y, line in enumerate(data.splitlines()):
            for mo in self.NUM_PATTERN.finditer(line):
                span = mo.span()
                for x in range(span[0], span[1]):
                    self.number_grid[Point(x,y)] = int(mo[0])

    def symbols_from_str(self, data:str):
        for y, line in enumerate(data.splitlines()):
            for mo in self.SYMBOL_PATTERN.finditer(line):
                self.symbol_grid[Point(mo.start(),y)] = mo[0]
            

def solve_a(data:str) -> int:
    pg = Partgrid()
    pg.numbers_from_str(data)
    pg.symbols_from_str(data)
    running_sum = 0
    for point, _ in pg.symbol_grid.items():
        nbs = neighbours(point)
        nums = [pg.number_grid.get(p, 0) for p in nbs]
        nums = list(set(nums)) # Assumtion: Safe to remove duplicates
        running_sum += sum(nums)
    return running_sum

def solve_b(data:str) -> int:
    pg = Partgrid()
    pg.numbers_from_str(data)
    pg.symbols_from_str(data)
    running_sum = 0
    for point, sym in pg.symbol_grid.items():
        if sym == '*':
            nbs = neighbours(point)
            nums = [pg.number_grid.get(p, None) for p in nbs]
            nums = list(set(nums)) # Assumtion: Safe to remove duplicates
            nums = [num for num in nums if num]
            if len(nums) == 2:
                running_sum += nums[0]*nums[1]
    return running_sum


if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=3)

    example_a = solve_a(puzzle.example_data)
    assert (example_a == 4361)
    puzzle.answer_a = solve_a(puzzle.input_data)

    example_b = solve_b(puzzle.example_data)
    assert(example_b == 467835)
    puzzle.answer_b = solve_b(puzzle.input_data)