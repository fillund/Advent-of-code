from aocd.models import Puzzle
import utils
from collections import defaultdict
import itertools as it
import numpy as np




def solve_a(data:str):
    grid = utils.parse_grid(data)
    frequencies = set(grid.values()) - set('.')
    bbox = utils.bounding_box(grid.keys())
    antinodes: dict[utils.Point, list] = defaultdict(list)
    for freq in frequencies:
        points = [k for k,v in grid.items() if v == freq]
        for pair in it.combinations(points, 2):
            nd_1 = np.array((pair[1].x, pair[1].y))
            nd_0 = np.array((pair[0].x, pair[0].y))
            A_B_vector = nd_1 - nd_0
            node_1 = nd_0 - A_B_vector
            node_2 = nd_1 + A_B_vector
            if bbox.Min_x <= node_1[0] <= bbox.Max_x and bbox.Min_y <= node_1[1] <= bbox.Max_y:
                antinodes[utils.Point(node_1[0], node_1[1])].append(freq)
            if bbox.Min_x <= node_2[0] <= bbox.Max_x and bbox.Min_y <= node_2[1] <= bbox.Max_y:
                antinodes[utils.Point(node_2[0], node_2[1])].append(freq)

    return len(antinodes)
    
def solve_b(data:str):
    grid = utils.parse_grid(data)
    frequencies = set(grid.values()) - set('.')
    bbox = utils.bounding_box(grid.keys())
    antinodes: dict[utils.Point, list] = defaultdict(list)
    for freq in frequencies:
        points = [k for k,v in grid.items() if v == freq]
        if len(points) > 1:
            for p in points:
                antinodes[p].append(freq)
                
        for pair in it.combinations(points, 2):
            done_0 = False
            done_1 = False
            n = 0
            while not (done_0 and done_1):
                n += 1
                nd_1 = np.array((pair[1].x, pair[1].y))
                nd_0 = np.array((pair[0].x, pair[0].y))
                A_B_vector = nd_1 - nd_0
                node_1 = nd_0 - n*A_B_vector
                node_2 = nd_1 + n*A_B_vector
                if bbox.Min_x <= node_1[0] <= bbox.Max_x and bbox.Min_y <= node_1[1] <= bbox.Max_y:
                    antinodes[utils.Point(node_1[0], node_1[1])].append(freq)
                else:
                    done_0 = True
                if bbox.Min_x <= node_2[0] <= bbox.Max_x and bbox.Min_y <= node_2[1] <= bbox.Max_y:
                    antinodes[utils.Point(node_2[0], node_2[1])].append(freq)
                else:
                    done_1 = True

    return len(antinodes)
                


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=8)

    example_a = solve_a(puzzle.example_data)
    assert (example_a == 14)
    answer_a = solve_a(puzzle.input_data)
    puzzle.answer_a = answer_a

    example_b = solve_b(puzzle.example_data)
    assert (example_b == 34)
    answer_b = solve_b(puzzle.input_data)
    puzzle.answer_b = answer_b
    