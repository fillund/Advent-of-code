from aocd.models import Puzzle
from typing import List, Dict, Tuple
from itertools import product

TEST_DATA = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

class Octopus:
    def __init__(self, energy:int) -> None:
        self.energy = energy
        self.flashed = False

    def reset_flash(self):
        self.flashed = False

    def add_energy(self):
        self.energy += 1
        if self.energy > 9:
            self.flashed = True
        return self.flashed
        
def solve_a(lines:List):
    grid = {}
    total = 0
    for y, line in enumerate(lines):
        for x, val in enumerate(line):
            grid[(x,y)] = Octopus(int(val))
    
    return simulate(grid, 100)

def solve_b(lines:List):
    grid = {}
    for y, line in enumerate(lines):
        for x, val in enumerate(line):
            grid[(x,y)] = Octopus(int(val))
    num_oct = len(grid)
    steps = 1
    while simulate(grid, 1) != num_oct:
        steps += 1
    return steps

def simulate(grid:Dict[Tuple[int,int], Octopus],steps:int):
    num_flashes = 0
    for i in range(steps):
        flashed = set()
        to_flash = []
        for c, octp in grid.items():
            octp.reset_flash()
            if octp.add_energy():
                to_flash.append(c)
        while to_flash:
            c = to_flash.pop()
            if c not in flashed:
                flashed.add(c)
                for n in neighbours(*c):
                    if grid[n].add_energy():
                        to_flash.append(n)

        for c in flashed:
            grid[c].energy = 0

        num_flashes += len(flashed)
    return num_flashes

def neighbours(x, y):
    xs = range(-1, 2)
    ys = range(-1, 2)
    coords = [(x+dx, y+dy) for dx, dy in product(xs, ys) if (dx, dy) != (0,0)]
    inrange = lambda c: coord_in_range(c[0], c[1])
    return list(filter(inrange, coords))

def coord_in_range(x, y):
    return 0<=x<=9 and 0<=y<=9

if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=11)
    print(neighbours(1,1))
    test_ans = solve_a(TEST_DATA.splitlines())
    assert(test_ans == 1656)
    puzzle.answer_a = solve_a(puzzle.input_data.splitlines())

    test_ans = solve_b(TEST_DATA.splitlines())
    assert(test_ans == 195)

    puzzle.answer_b = solve_b(puzzle.input_data.splitlines())
