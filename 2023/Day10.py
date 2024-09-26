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

    count = 0
    # For all coords within bounding box, not in visited: 
    #    Check lines in x and y to edge of BB. 
    #If the line crosses the network odd times, it is enclosed

    return 0

example_data = """.....
.S-7.
.|.|.
.L-J.
....."""

if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=10)

    example_a = solve_a(example_data)
    assert (example_a == 4)
    puzzle.answer_a = solve_a(puzzle.input_data)
