from typing import Iterable
from itertools import tee
from dataclasses import dataclass
import re
from math import sqrt
from collections import namedtuple

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
    Bbox = namedtuple("BoundingBox", ["Min_x", "Max_x", "Min_y", "Max_y"])
    return Bbox(min_x, max_x, min_y, max_y)

def numbers(string:str):
    return list(map(int, re.findall(r'\d+', string)))