from aocd.models import Puzzle
import utils
from utils import Point
from dataclasses import dataclass
import itertools as it
from collections import Counter
from tqdm import tqdm

@dataclass(unsafe_hash=True)
class Region():
    id:int
    label:str
    points:set[Point]
    def __init__(self, id, label, points=None) -> None:
        self.id = id
        self.label = label
        self.points = set(points) if points else set()
    def __contains__(self, item):
        return item in self.points

    def __len__(self):
        return len(self.points)
    
    def __eq__(self, value: "Region") -> bool:
        return self.id == value.id

    def add(self, p:Point):
        self.points.add(p)

    def neighbours(self) -> set[Point]:
        neighbours = set()
        for p in self.points:
            neighbours |= {pn for pn in p.cardinal_neighbours()}
        return neighbours-self.points

    def perimiter(self):
        region_per = 0
        for p in self.points:
            block_per = 0
            for pn in p.cardinal_neighbours():
                if pn not in self.points:
                    block_per += 1
            region_per += block_per
        return region_per

    def area(self):
        return len(self.points)

def solve_a(data:str):
    grid = utils.parse_grid(data)
    regions:list[Region] = []
    explored: set[Point] = set()
    next_id = 0
    # Go through entire grid
    for p, v  in grid.items():
        #Skip explored
        if p in explored:
            continue
        q = [p]
        # Create new region. Must be new region, since regions are explored entirely before moving on.
        r = Region(next_id, v, None)
        next_id += 1
        #Explore new region
        while len(q) > 0:
            current = q.pop()
            explored.add(current)
            if grid[current] == v:
                r.add(current)
            q.extend([pn for pn in current.cardinal_neighbours() if grid.get(pn, None) == v and pn not in explored])
        regions.append(r)

    return sum([r.area()*r.perimiter() for r in regions])
    
def solve_b(data:str):
    pass
                
EXAMPLE = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

def test_1():
    data = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO"""
    test = solve_a(data)
    assert (test == 772)

def test_2():
    data = """AAAA
BBCD
BBCC
EEEC"""
    test = solve_a(data)
    assert (test==140)


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=12)
    test_1()
    test_2()
    example_a = solve_a(EXAMPLE)
    assert (example_a == 1930)
    answer_a = solve_a(puzzle.input_data)
    puzzle.answer_a = answer_a

    example_b = solve_b(puzzle.example_data)
    assert (example_b == 48)
    answer_b = solve_b(puzzle.input_data)
    puzzle.answer_b = answer_b
    