from typing import Iterable
from itertools import tee
from dataclasses import dataclass
import re
from math import sqrt

@dataclass
class Point():
    x:int
    y:int
    def __hash__(self):
        return hash((self.x, self.y))
    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False
    def L2(self, other:"Point"):
        # Euclidean distance to other point
        return sqrt((self.x-other.x)**2 + (self.y-other.y)**2)
    def L1(self, other:"Point"):
        # Manhattan distance to other point
        return abs(self.x-other.x)+abs(self.y-other.y)

def nwise(iterable:Iterable, n:int)->Iterable[tuple]:
    iters = tee(iterable, n)
    for i, iterator in enumerate(iters):
        for _ in range(i):
            next(iterator, None)
    return zip (*iters)

def grouper(iterable, n):
    "Return groups of n"
    args = [iter(iterable)]*n
    return list(zip(*args))

def parse_grid(data:str) -> dict[Point, str]:
    grid: dict[Point, str] = {}
    for y, line in enumerate(data.splitlines()):
        for x, char in enumerate(line):
            grid[Point(x, y)] = char
    return grid

def plot_grid(original:dict[Point, str], markers:dict[Point, str]={}):
    assert(all([k in original for k in markers.keys()]))
    bb = bounding_box(original.keys())
    lines = []
    for row in range(bb[2], bb[3]+1):
        sorted_row = sorted(filter(lambda i: i[0].y == row, original.items()), key=lambda i: i[0].x)
        line = [markers[a[0]] if a[0] in markers else a[1] for a in sorted_row]
        lines.append(''.join(line))
        # for item in sorted_row:

        #     char = item[1]
        #     if item[0] in markers:
        #         char = markers[item[0]]
    return '\n'.join(lines)



def neighbours(point: Point) -> list[Point]:
    offsets = (-1, 0, 1)
    out = []
    for ox in offsets:
        for oy in offsets:
            if (ox, oy) != (0,0):
                out.append(Point(point.x + ox, point.y + oy))
    return out

def bounding_box(points:Iterable[Point]):
    min_x = min((p.x for p in points))
    max_x = max((p.x for p in points))
    min_y = min((p.y for p in points))
    max_y = max((p.y for p in points))
    return (min_x, max_x, min_y, max_y)

def numbers(string:str):
    return list(map(int, re.findall(r'\d+', string)))