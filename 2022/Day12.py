import itertools as it
from aocd.models import Puzzle
from typing import List, Dict, Tuple, Set
from collections import Counter, defaultdict
from math import inf, sqrt
from bisect import insort
import heapq as hq

class Graph:
    def __init__(self, lines:List[str]) -> None:
        nodes = {}
        self.lowpoints = []
        for y, line in enumerate(lines):
            for x, value in enumerate(line):
                if value == 'S':
                    self.start = (x,y)
                    nodes[(x,y)] = ord('a')
                elif value == 'E':
                    self.goal = (x,y)
                    nodes[(x,y)] = ord('z')
                elif value == 'a':
                    self.lowpoints.append((x,y))
                    nodes[(x,y)] = ord(value)
                else:
                    nodes[(x,y)] = ord(value)
        self.width = max((a[0] for a in nodes.keys())) +1
        self.height = max((a[1] for a in nodes.keys())) +1
        self.corner = (self.width-1, self.height-1)
        self.nodes = nodes
        transitions = self._create_trans(nodes)
        self.neighbours = transitions

    def _create_trans(self, nodes:Dict[tuple[int, int], int]):
        transitions = defaultdict(list)
        for node in nodes.items():
            x, y = node[0]
            this_val = node[1]
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                x2 = x+dx
                y2 = y+dy
                if 0<=x2<self.width and 0<=y2<self.height and self.nodes[(x2,y2)]<=this_val+1:
                    transitions[(x, y)].append((x2, y2))
        return transitions

    def plot_path(self, path):
        out = []
        for y in range(self.corner[1]+1):
            for x in range(self.corner[0]+1):
                if (x,y) in path:
                    out.append(chr(self.nodes[(x,y)]))
                else:
                    out.append('.')
            out.append('\n')
        with open(str(self.width), 'w') as f:
            f.write(''.join(out))

    def __str__(self):
        out = []
        for y in range(self.corner[1]+1):
            for x in range(self.corner[0]+1):
                out.append(str(self.nodes[(x,y)]))
            out.append('\n')
        return ''.join(out).rstrip()

def heuristic(p1, p2):
    return sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
    # return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

def shortest_path(g:Graph, start:Tuple[int, int], target:Tuple[int, int]):

    q = [(0, start)]
    dist = {k:inf for k in g.nodes.keys()} # The actual distance
    visited = set()
    # score = {k:inf for k in g.nodes.keys()}
    # score[start] = heuristic(start, target) # The one to sort by
    dist[start] = 0
    prev = {}
    while q:
        # r, u = q.pop(0)
        r, u = hq.heappop(q)
        visited.add(u)
        # if u == target:
        #     break

        for v in g.neighbours[u]:
            alt = r + 1 #g.nodes[v]
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                # score[v] = alt + heuristic(v, target)
                if v not in visited:
                    hq.heappush(q, (dist[v], v))
    path = recreate_path(prev, target)
    # print(path)
    # print([g.nodes[k] for k in path])
    g.plot_path(path)
    return dist[target]

def recreate_path(cameFrom:dict, target):
    path = [target]
    current = target
    while current in cameFrom:
        current = cameFrom[current]
        path.insert(0, current)
    return path



if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=12)
    example_graph = Graph(puzzle.example_data.splitlines())
    example_a = shortest_path(example_graph, (example_graph.start), example_graph.goal)
    assert(example_a == 31)
    
    graph = Graph(puzzle.input_data.splitlines())
    answer_a = shortest_path(graph, graph.start, graph.goal)
    puzzle.answer_a = answer_a

    # This would have already been done if I did BFS instead. Oh well.
    example_b = min([shortest_path(g, p, g.goal) for g,p in zip(it.repeat(example_graph), example_graph.lowpoints)])
    assert(example_b == 29)
    answer_b = min([shortest_path(g, p, g.goal) for g,p in zip(it.repeat(graph), graph.lowpoints)])
    puzzle.answer_b = answer_b