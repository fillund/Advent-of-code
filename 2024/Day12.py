from aocd.models import Puzzle
import utils
from utils import Point
from dataclasses import dataclass
import itertools as it
from collections import Counter
from tqdm import tqdm
from enum import Enum, auto

class SweepState(Enum):
    INSIDE = auto()
    OUTSIDE = auto()

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

    def sides(self):
        sides = 4 # Must at least bound a box
        bbox = utils.bounding_box(self.points)
        # Vertical sweep, check x+-1
        for x in range(bbox.Min_x, bbox.Max_x+1):
            # TODO: Check start condition
            left_state = SweepState.INSIDE if Point(x-1, bbox.Min_y) in self.points else SweepState.OUTSIDE
            right_state = SweepState.INSIDE if Point(x+1, bbox.Min_y) in self.points else SweepState.OUTSIDE
            for y in range(bbox.Min_y, bbox.Max_y+1):
                p = Point(x,y)
                left = Point(x-1, y)
                right = Point(x+1, y)
                if p not in self.points:
                    ## Skip checks if outside to not double count
                    if left not in self.points:
                        left_state = SweepState.OUTSIDE
                    else:
                        left_state = SweepState.INSIDE
                    if right not in self.points:
                        right_state = SweepState.OUTSIDE
                    else:
                        right_state = SweepState.INSIDE
                    continue
                # Check left
                if left_state == SweepState.INSIDE and left not in self.points:
                    sides += 1
                    left_state = SweepState.OUTSIDE
                elif left_state == SweepState.OUTSIDE and left in self.points:
                    left_state = SweepState.INSIDE
                # Check right
                if right_state == SweepState.INSIDE and right not in self.points:
                    sides += 1
                    right_state = SweepState.OUTSIDE
                elif right_state == SweepState.OUTSIDE and right in self.points:
                    right_state = SweepState.INSIDE
        # Horizontal sweep
        for y in range(bbox.Min_y, bbox.Max_y+1):
            up_state = SweepState.INSIDE if Point(bbox.Min_x, y-1) in self.points else SweepState.OUTSIDE
            down_state = SweepState.INSIDE if Point(bbox.Min_x, y+1) in self.points else SweepState.OUTSIDE
            for x in range(bbox.Min_x, bbox.Max_x+1):
                p = Point(x,y)
                if p not in self.points:
                    # Skip checks if outside to not double count
                    if up not in self.points:
                        up_state = SweepState.OUTSIDE
                    else:
                        up_state = SweepState.INSIDE
                    if down not in self.points:
                        down_state = SweepState.OUTSIDE
                    else:
                        down_state = SweepState.INSIDE
                    continue
                up = Point(x, y-1)
                down = Point(x, y+1)
                # Check up
                if up_state == SweepState.INSIDE and up not in self.points:
                    sides += 1
                    up_state = SweepState.OUTSIDE
                elif up_state == SweepState.OUTSIDE and up in self.points:
                    up_state = SweepState.INSIDE
                # Check down
                if down_state == SweepState.INSIDE and down not in self.points:
                    sides += 1
                    down_state = SweepState.OUTSIDE
                elif down_state == SweepState.OUTSIDE and down in self.points:
                    down_state = SweepState.INSIDE
        return sides

    def area(self):
        return len(self.points)

def make_regions(grid):
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
    return regions

def solve_a(data:str):
    grid = utils.parse_grid(data)
    regions = make_regions(grid)
    return sum([r.area()*r.perimiter() for r in regions])
    
def solve_b(data:str):
    grid = utils.parse_grid(data)
    regions = make_regions(grid)
    for r in regions:
        print(f"Plant {r.label} Area {r.area()} Sides {r.sides()}")
    return sum([r.area()*r.sides() for r in regions])


                
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

def test_AB():
    data = """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA"""
    test = solve_b(data)
    assert(test==368)

def test_E():
    data = """EEEEE
EXXXX
EEEEE
EXXXX
EEEEE"""
    test = solve_b(data)
    assert(test==236)

if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=12)
    test_1()
    test_2()
    example_a = solve_a(EXAMPLE)
    assert (example_a == 1930)
    answer_a = solve_a(puzzle.input_data)
    puzzle.answer_a = answer_a
    test_AB()
    test_E()
    example_b = solve_b(EXAMPLE)
    assert (example_b == 1206)
    answer_b = solve_b(puzzle.input_data)
    puzzle.answer_b = answer_b
    