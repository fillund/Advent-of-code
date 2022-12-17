import itertools as it
from aocd.models import Puzzle
from typing import List, Dict, Tuple, Set
from tqdm import tqdm
import numpy as np
from Day5 import numbers

def parse(line:str) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    nums = numbers(line)
    sensor = (nums[0], nums[1])
    beacon = (nums[2], nums[3])
    return (sensor, beacon)

# Naive implementation, for the lulz.
def coverage(sensor, beacon, target_row):
    s = np.array(sensor)
    b = np.array(beacon)
    vec = s-b
    dist = int(np.linalg.norm(vec, ord=1))
    height_diff = abs(s[1]-target_row)
    x_min = sensor[0]-dist+height_diff
    x_max = sensor[0]+dist-height_diff
    y_min = sensor[1]-dist
    y_max = sensor[1]+dist
    if y_min>target_row or y_max<target_row:
        return set()
    print(f"Coverage: {x_max-x_min} blocks")
    row = range(x_min, x_max+1)
    # cov = (x for x in row if x[1]==target_row and np.linalg.norm(x-s, ord=1) <= dist)
    return set(range(x_min, x_max)) - {beacon}


def part_a(input:str, target_row):
    pairs = list(map(parse, input.splitlines()))
    total_cov = set()
    for s,b in tqdm(pairs):
        total_cov |= coverage(s,b, target_row)
        # total_cov -= {s[0]}
        # total_cov -= {b[0]}
    
    return len([x for x in total_cov])

def part_b(input:str):
    pairs = list(map(parse, input.splitlines()))
    

if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=15)

    print(part_a(puzzle.example_data, 10))
    

    puzzle.answer_a = part_a(puzzle.input_data, 2000000)