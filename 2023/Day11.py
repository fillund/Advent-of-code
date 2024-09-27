from dataclasses import dataclass
from aocd.models import Puzzle
from utils import Point, parse_grid, bounding_box
import itertools as it
from typing import Iterable



def solve_a(data:str):
    grid_in = parse_grid(data)
    galaxy_points_in = {k for k,v in grid_in.items() if v=='#'}
    #Expand galaxy
    #Find empty columns
    empty_columns = []
    (min_x, max_x, min_y, max_y) = bounding_box(grid_in)


    #Create pairs


    #Manhattan distance between all pairs
    
    return 0


def solve_b(data:str):
    return 0


if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=10)

    # example_a = solve_a(example_data)
