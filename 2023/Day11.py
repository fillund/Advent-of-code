from dataclasses import dataclass
from aocd.models import Puzzle
from utils import Point, parse_grid, bounding_box
import itertools as it
from typing import Iterable



def solve_a(data:str, expansion=1):
    grid_in = parse_grid(data)
    galaxy_points_in = {k for k,v in grid_in.items() if v=='#'}
    #Find empty columns
    (min_x, max_x, min_y, max_y) = bounding_box(grid_in)
    empty_columns = set(range(min_x, max_x+1))
    empty_rows = set(range(min_y, max_y+1))
    occupied_rows = set()
    occupied_columns = set()
    for gp in galaxy_points_in:
        empty_columns.discard(gp.x)
        empty_rows.discard(gp.y)
        occupied_columns.add(gp.x)
        occupied_rows.add(gp.y)

    #Expand galaxy
    galaxy:set[Point] = set()
    for gp in galaxy_points_in:
        galaxies_to_the_left = len([gx for gx in occupied_columns if gx<gp.x])
        galaxies_above = len([gy for gy in occupied_rows if gy<gp.y])
        columns_before = len([x for x in empty_columns if x<gp.x])
        rows_before = len([y for y in empty_rows if y<gp.y])
        new_point = Point(galaxies_to_the_left+columns_before*(expansion+1),
                          galaxies_above+rows_before*(expansion+1))
        galaxy.add(new_point)
    #Create pairs
    assert(len(galaxy_points_in) == len(galaxy))
    pairs = list(it.combinations(galaxy, 2))

    #Manhattan distance between all pairs
    lengths = sum([pair[0].L1(pair[1]) for pair in pairs])
    
    return lengths




if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=11)

    example_a = solve_a(puzzle.example_data)
    assert(example_a == 374)
    answer_a = solve_a(puzzle.input_data)
    puzzle.answer_a = answer_a
    example_b_1 = solve_a(puzzle.example_data, 10)
    assert(example_b_1 == 1030)
    example_b_2 = solve_a(puzzle.example_data, 100)
    assert(example_b_2 == 8410)
