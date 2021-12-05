from aocd.models import Puzzle
from collections import namedtuple
from collections import Counter
from itertools import chain
from typing import List

Point = namedtuple('Point', ['x', 'y'])

# Line = namedtuple('Line', ['p1', 'p2'])

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        if self.p1.x < self.p2.x:
            self.dirx = 1
        else:
            self.dirx = -1
        if self.p1.y < self.p2.y:
            self.diry = 1
        else:
            self.diry = -1
        self.length = max(abs(self.p1.x - self.p2.x), abs(self.p1.y - self.p2.y))

    def get_points(self):
        if self.is_horizontal():
            start_x = min(self.p1.x, self.p2.x) +1 # Add 1 to not count a point twice
            stop_x = max(self.p1.x, self.p2.x)
            points = [Point(x, self.p1.y) for x in range(start_x, stop_x)]

        elif self.is_vertical():
            start_y = min(self.p1.y, self.p2.y) + 1
            stop_y = max(self.p1.y, self.p2.y)
            points = [Point(self.p1.x, y) for y in range(start_y, stop_y)]
        else:
            offsets = [(self.dirx*i, self.diry*i) for i in range(1, self.length)]
            points = [Point(self.p1.x+dx, self.p1.y+dy) for (dx, dy) in offsets]
        points.extend([self.p1, self.p2])
        return points

    def is_horizontal(self):
        return self.p1.y == self.p2.y

    def is_vertical(self):
        return self.p1.x == self.p2.x

def count_points_on_grid(lines: List[Line])-> Counter:
    all_points = [x.get_points() for x in lines if x.is_horizontal() or x.is_vertical()]
    counter = Counter(chain.from_iterable(all_points))
    return counter

def count_points_on_grid_diagonal(lines: List[Line])-> Counter:
    all_points = [x.get_points() for x in lines]
    counter = Counter(chain.from_iterable(all_points))
    return counter


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=5)

    data = puzzle.input_data.splitlines()
    lines = []
    for line in data:
        temp = line.split('->')
        temp1 = [int(x) for x in temp[0].split(',')]
        temp2 = [int(x) for x in temp[1].split(',')]
        p1 = Point(*temp1)
        p2 = Point(*temp2)
        lines.append(Line(p1,p2))
    
    counter = count_points_on_grid(lines)
    num_crosses = 0
    for val in counter.values():
        if val >= 2:
            num_crosses += 1

    puzzle.answer_a = num_crosses

    counter = count_points_on_grid_diagonal(lines)
    num_crosses = 0
    for val in counter.values():
        if val >= 2:
            num_crosses += 1

    puzzle.answer_b = num_crosses

