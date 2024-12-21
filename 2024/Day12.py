from aocd.models import Puzzle
import utils
from utils import Point
from dataclasses import dataclass, field

@dataclass
class Region():
    label:str
    _points:set[Point]
    def __init__(self, label, points=None) -> None:
        self.label = label
        self._points = set(points) if points else set()
    def __contains__(self, item):
        return item in self._points

    def add(self, p:Point):
        self._points.add(p)
        # Sanity check
        if len(self._points)>1:
            assert any([pn in self._points for pn in p.cardinal_neighbours()])

    def neighbours(self) -> set[Point]:
        neighbours = set()
        for p in self._points:
            neighbours |= {pn for pn in p.cardinal_neighbours()}
        return neighbours-self._points

    def perimiter(self):
        region_per = 0
        for p in self._points:
            block_per = 0
            for pn in p.cardinal_neighbours():
                if pn not in self._points:
                    block_per += 1
            region_per += block_per
        return region_per

    def area(self):
        return len(self._points)


def solve_a(data:str):
    grid = utils.parse_grid(data)
    regions:list[Region] = []
    for p, v in grid.items():
        found = False
        for r in regions:
            if v == r.label and p in r.neighbours():
                r.add(p)
                found = True
                break
        if not found:
            regions.append(Region(v, [p]))
    # TODO: Merge regions
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

if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=12)
    example_a = solve_a(EXAMPLE)
    assert (example_a == 1930)
    answer_a = solve_a(puzzle.input_data)
    puzzle.answer_a = answer_a

    example_b = solve_b(puzzle.example_data)
    assert (example_b == 48)
    answer_b = solve_b(puzzle.input_data)
    puzzle.answer_b = answer_b
    