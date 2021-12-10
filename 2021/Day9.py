from collections import defaultdict
from aocd.models import Puzzle
from typing import List, Dict
from functools import reduce
import operator

TEST_DATA = """2199943210
3987894921
9856789892
8767896789
9899965678"""
TEST_SUM_RISK = 15


class Grid:
    def __init__(self, lines:List[str]) -> None:
        self.grid = {}
        for y, line in enumerate(lines):
            for x, val in enumerate(line):
                self.grid[(x,y)] = int(val)

    def get_neighbours(self, x, y):
        return [self.grid.get((x+1, y), 9), self.grid.get((x-1, y), 9), self.grid.get((x, y+1), 9), self.grid.get((x, y-1), 9)]

    def get_neighbours_cells(self, x, y):
        return [(x+1, y), (x-1, y),(x, y+1), (x, y-1)]


    def keys(self):
        return self.grid.keys()

    def values(self):
        return self.grid.values()

    def items(self):
        return self.grid.items()

    def __getitem__(self, key):
        return self.grid.get(key, 9)


def solve_a(grid:Grid):
    low_points = []
    for cell, value in grid.items():
        if all([value < x for x in grid.get_neighbours(*cell)]):
            low_points.append(cell)
    
    return sum([grid[k]+1 for k in low_points])


def solve_b(grid:Grid):
    low_points = []
    for cell, value in grid.items():
        if all([value < x for x in grid.get_neighbours(*cell)]):
            low_points.append(cell)
    print("Found all low points")
    basin_sizes = []
    for i, lp in enumerate(low_points):
        size = find_basin_size(grid, *lp)
        basin_sizes.append(size)
        print(f"Found basin number {i} of {size=}")


    basin_sizes.sort(reverse=True)
    return reduce(operator.mul, basin_sizes[:3])

# We can assume a basin is unique
def find_basin_size(grid:Grid, x ,y):
    to_explore = [a for a in grid.get_neighbours_cells(x, y) if grid[a] != 9] # TODO
    explored = {(x, y)}
    while to_explore:
        cell = to_explore.pop()
        explored.add(cell)
        neighbours = [a for a in grid.get_neighbours_cells(*cell) if grid[a] != 9]
        to_explore.extend([a for a in neighbours if a not in explored])
    # print(explored)
    return len(explored)





if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=9)
    data = puzzle.input_data
    grid = Grid(data.splitlines())
    puzzle.answer_a = solve_a(grid)
    puzzle.answer_b = solve_b(grid)
    # test_grid = Grid(TEST_DATA.splitlines())
    # print(solve_b(test_grid))
