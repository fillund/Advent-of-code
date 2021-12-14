from aocd.models import Puzzle
from typing import List, Dict, Tuple, Set

TEST_DATA = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""


def get_data_and_instructions(lines:List[str]):
    coords_parse = True
    coords = []
    instructions = []
    for line in lines:
        if line == '':
            coords_parse = False
            continue
        if coords_parse:
            x,y = line.split(',')
            coords.append((int(x), int(y)))
        else:
            inst = line.removeprefix("fold along ")
            d, _, val = inst.partition('=')
            instructions.append((d, int(val)))
    return (set(coords), instructions)


def solve_a(grid: Set[Tuple[int,int]], instructions:List[Tuple[str, int]]):
    grid_a = grid

    grid_a = fold(grid_a, *instructions[0])
    return len(grid_a), grid_a

def solve_b(grid: Set[Tuple[int,int]], instructions:List[Tuple[str, int]]):
    outgrid = grid
    for inst in instructions:
        outgrid = fold(outgrid, *inst)
    return outgrid
        

def fold(grid: Set[Tuple[int,int]], axis:str, coord:int)->Set[Tuple[int,int]]:
    if axis == 'x':
        ax = 0
    else:
        ax = 1
    bound = max((c[ax] for c in grid))
    # print(bound)
    keep = {c for c in grid if c[ax]<coord}
    other = grid-keep
    if axis == 'x':
        flipped = {(coord-abs(coord-x), y) for x,y in other}
    elif axis == 'y':
        flipped = {(x, coord-abs(coord-y)) for x,y in other}

    folded = keep | flipped
    return folded

def pretty(grid: Set[Tuple[int, int]]):
    width = max((c[0] for c in grid))+1
    height = max((c[1] for c in grid))+1
    CHAR_WIDTH = 4
    out = []
    for y in range(height):
        for x in range(width):
            if x % CHAR_WIDTH == 0:
                out.append('')
            if (x, y) in grid:
                out.append(' #')
            else:
                out.append(' .')
        out.append('\n')
    return ''.join(out)
            


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=13)
    grid, instructions = get_data_and_instructions(TEST_DATA.splitlines())
    # print(pretty(grid))
    ans, out_grid = solve_a(grid, instructions) 
    # print(pretty(out_grid))
    assert(ans == 17)

    # grid, instructions = get_data_and_instructions(puzzle.input_data.splitlines())
    ans, out_grid = solve_a(grid, instructions)
    # # print(pretty(out_grid))
    puzzle.answer_a = ans

    grid, instructions = get_data_and_instructions(puzzle.input_data.splitlines())
    out_grid = solve_b(grid, instructions)
    print(pretty(out_grid))
    with open('out13.txt', 'w') as f: # print to file for easier reading
        f.write(pretty(out_grid))
 



