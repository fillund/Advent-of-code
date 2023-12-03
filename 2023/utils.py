from typing import Iterable
from itertools import tee
from typing import NamedTuple

Point = NamedTuple('Point', [('x', int), ('y', int)])

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