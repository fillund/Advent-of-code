from enum import Enum
from aocd.models import Puzzle
import itertools as it
from typing import Dict, List, Sequence

puzzle = Puzzle(2022, 8)


def read_grid(data:str):
    grid = {}
    for row, line in enumerate(data.splitlines()):
        for col, char in enumerate(line):
            grid[(col, row)] = int(char)
    return grid

def is_visible(grid:Dict[tuple, int], x: int, y: int):
    maxc, maxr = list(grid)[-1]
    tree = grid[(x,y)]
    if x == 0 or y == 0 or x == maxc or y == maxr:
        return True
    above = (tree > grid[a] for a in grid if a[0] == x and a[1] > y)
    below = (tree > grid[a] for a in grid if a[0] == x and a[1] < y) 
    left = (tree > grid[a] for a in grid if a[1] == y and a[0] < x)
    right = (tree > grid[a] for a in grid if a[1] == y and a[0] > x)
    return any([all(above), all(below), all(left), all(right)])

def seen_trees(curr_val: int, trees:Sequence[int]):
    seen = 0
    if len(trees) == 0:
        return 0
    for tree in trees:
        seen += 1
        if tree >= curr_val:
            break
    return seen


def scenic_score(grid:Dict[tuple, int], x: int, y: int):
    maxc, maxr = list(grid)[-1]
    tree = grid[(x,y)]
    if x == 0 or y == 0 or x == maxc or y == maxr:
        return 0
    below = seen_trees(tree, [grid[c,r] for c,r in grid if c == x and r > y])
    above = seen_trees(tree, list(reversed([grid[c,r] for c,r in grid if c == x and r < y])))
    right = seen_trees(tree, [grid[c,r] for c,r in grid if r == y and c > x])
    left = seen_trees(tree,  list(reversed([grid[c,r] for c,r in grid if r == y and c < x])))
    return above*below*left*right

example_grid = read_grid(puzzle.example_data)
example_a = sum(map(lambda arg: is_visible(example_grid, *arg), example_grid))

assert(example_a == 21)

grid_a = read_grid(puzzle.input_data)
answer_a = sum(map(lambda arg: is_visible(grid_a, *arg), grid_a))
puzzle.answer_a = answer_a

assert(scenic_score(example_grid, 2, 1) == 4)
assert(scenic_score(example_grid, 2, 3) == 8)
assert(scenic_score(example_grid, 3, 3) == 3)

example_b = max(map(lambda arg: scenic_score(example_grid, *arg), example_grid))
assert(example_b == 8)
answer_b = max(map(lambda arg: scenic_score(grid_a, *arg), grid_a))
puzzle.answer_b = answer_b