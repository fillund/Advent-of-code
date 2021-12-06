from aocd.models import Puzzle
from typing import List, Tuple


def parse_commands(inputs : List[str]) -> Tuple[int, int]:
    dist = 0
    depth = 0

    for line in inputs:
        com, _, x = line.partition(' ')
        x = int(x)
        if 'forward' in com:
            dist = dist + x
        elif 'down' in com:
            depth = depth + x
        elif 'up' in com:
            depth = depth - x
    
    return (dist, depth)

def parse_commands2(inputs : List[str]) -> Tuple[int, int]:
    dist = 0
    depth = 0
    aim = 0

    for line in inputs:
        com, _, x = line.partition(' ')
        x = int(x)
        if 'forward' in com:
            dist = dist + x
            depth = depth + aim * x
        elif 'down' in com:
            aim = aim + x
        elif 'up' in com:
            aim = aim - x
    
    return (dist, depth)




if __name__ == "__main__":
    # puzzle = Puzzle(year=2021, day=2)

    # lines = puzzle.input_data
    with open('2021/Day2.txt') as f:
        lines = f.readlines()


    (dist, depth) = parse_commands(lines)
    print(f'{dist=}, {depth=}')
    print(f'Part1: {dist*depth}')

    (dist, depth) = parse_commands2(lines)
    print(f'{dist=}, {depth=}')
    print(f'Part2: {dist*depth}')
