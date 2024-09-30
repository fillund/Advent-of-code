from dataclasses import dataclass
from aocd.models import Puzzle
import utils
import itertools as it
from collections import namedtuple, deque

@dataclass
class Path:
    p:utils.Point
    cost:float

def solve_a(data:str):
    grid = utils.parse_grid(data)
    start = list(filter(lambda x: grid[x] == 'S', grid))[0]
    q = deque()

    q.append(Path(start, 0))
    visited = {}

    while len(q) > 0:
        pc:Path = q.popleft()
        current:utils.Point = pc.p
        cost:float = pc.cost
        if current in visited:
            continue

        visited[current] = cost

        for n in utils.neighbours(current):
            #Above
            if n.x == current.x and n.y < current.y and grid.get(n, '.') in '|7F' and grid[current] in 'S|LJ':
                q.append(Path(n, cost+1))
            #Below
            elif n.x == current.x and n.y > current.y and grid.get(n, '.') in '|LJ' and grid[current] in 'S|F7':
                q.append(Path(n, cost+1))
            #Left
            elif n.x < current.x and n.y == current.y and grid.get(n, '.') in '-LF' and grid[current] in 'S-7J':
                q.append(Path(n, cost+1))
            #Right
            elif n.x > current.x and n.y == current.y and grid.get(n, '.') in '-7J' and grid[current] in 'S-LF':
                q.append(Path(n, cost+1))




    return max(visited.values())

def solve_b(data:str):
    grid = utils.parse_grid(data)
    start = list(filter(lambda x: grid[x] == 'S', grid))[0]
    q = deque()

    q.append(Path(start, 0))
    visited:dict[utils.Point, float] = {}

    while len(q) > 0:
        pc:Path = q.popleft()
        current:utils.Point = pc.p
        cost:float = pc.cost
        if current in visited:
            continue

        visited[current] = cost

        for n in utils.neighbours(current):
            #Above
            if n.x == current.x and n.y < current.y and grid.get(n, '.') in '|7F' and grid[current] in 'S|LJ':
                q.append(Path(n, cost+1))
            #Below
            elif n.x == current.x and n.y > current.y and grid.get(n, '.') in '|LJ' and grid[current] in 'S|F7':
                q.append(Path(n, cost+1))
            #Left
            elif n.x < current.x and n.y == current.y and grid.get(n, '.') in '-LF' and grid[current] in 'S-7J':
                q.append(Path(n, cost+1))
            #Right
            elif n.x > current.x and n.y == current.y and grid.get(n, '.') in '-7J' and grid[current] in 'S-LF':
                q.append(Path(n, cost+1))

    # Calculate bounding box of network
    min_x = min([a.x for a in visited.keys()])
    max_x = max([a.x for a in visited.keys()])
    min_y = min([a.y for a in visited.keys()])
    max_y = max([a.y for a in visited.keys()])

    enclosed = []
    # For all coords within bounding box, not in visited: 
    #    Check lines in x to edge of BB. 
    #If the line crosses the network odd times, it is enclosed
    for (x,y) in it.product(range(min_x+1, max_x), range(min_y+1, max_y)):
        parity = 0
        # Is an interior point also part of the loop, skip
        if utils.Point(x,y) in visited:
            continue
        # Check direction as short as possible
        if abs(min_x-x) < abs(x-max_x):
            ro = range(min_x, x+1)
        else:
            ro = range(x, max_x+1)
        #Scan line    
        for scan_x in ro:
            tp = utils.Point(scan_x, y)
            parity += tp in visited and grid[tp] != '-'
        if isOdd(parity):
            enclosed.append((x,y))

    return len(enclosed)

def isOdd(num):
    return num%2 != 0

example_data = """.....
.S-7.
.|.|.
.L-J.
....."""

example_data_b = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""

example_data_b_2 = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""

example_data_b_3 = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""


if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=10)

    example_a = solve_a(example_data)
    assert (example_a == 4)
    puzzle.answer_a = solve_a(puzzle.input_data)

    assert(solve_b(example_data_b_3) == 4)
    assert(solve_b(example_data_b) == 8)
    assert(solve_b(example_data_b_2) == 10)
    puzzle.answer_b = solve_b(puzzle.input_data)