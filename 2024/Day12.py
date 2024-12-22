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
    next_id = 0
    print("Creating regions")
    for p, v in tqdm(grid.items()):
        found = False
        for r in regions:
            if v == r.label and p in r.neighbours():
                r.add(p)
                found = True
                break
        if not found:
            regions.append(Region(next_id, v, [p]))
            next_id+=1
    merged_regions = []
    merge_groups:list[list[int]] = []
    print("Creating merge groups")
    for r1, r2 in tqdm(it.combinations(regions, 2)):
        if r1.label == r2.label and r1.neighbours()&r2.points:
            found = False
            for group in merge_groups:
                if r1.id in group:
                    group.append(r2.id)
                    found = True
                    break
                elif r2.id in group:
                    group.append(r1.id)
                    found = True
                    break
            if not found:
                merge_groups.append([r1.id, r2.id])
    print("Merging regions")
    for group in merge_groups:
        regions_to_merge = [r for r in regions if r.id in group]
        points = []
        for r in regions_to_merge:
            points.extend(r.points)
            regions.remove(r)
        new_region = Region(regions_to_merge[0].id, regions_to_merge[0].label, points)
        regions.append(new_region)

    # print("Removing merged regions")
    # for rm in tqdm(regions.copy()):
    #     if rm.id in merged_regions:
    #         regions.remove(rm)
    all_points = []
    for r in regions:
        all_points.extend(r.points)
    counter = Counter(all_points)
    doubles = [p for p,c in counter.items() if c>1]
    print(doubles)
    assert(counter.total() == len(grid))
    for r in regions:
        print(f"Plant {r.label}: Area:{r.area()} Perimeter:{r.perimiter()} Score: {r.area()*r.perimiter()}")
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
    