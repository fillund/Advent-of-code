from typing import List, Tuple
from aocd.models import Puzzle
import re

REGEX = re.compile(r'(\d+)-(\d+),(\d+)-(\d+)')

puzzle = Puzzle(year=2022, day=4)

def get_sections(line) -> Tuple[int, int, int, int]:
    numbers = re.match(REGEX, line)
    assert(numbers)
    return tuple(int(a) for a in numbers.groups())

def is_subsection(section:Tuple[int, int, int, int]) -> bool:
    # First is contained in second
    if section[0]>=section[2] and section[1]<=section[3]:
        return True
    # Second is contained in first
    if section[0]<=section[2] and section[1]>=section[3]:
        return True
    return False
    
def overlaps(section:Tuple[int, int, int, int]) -> bool:
    if section[2] <= section[0] <= section[3]:
        return True
    if section[2] <= section[1] <= section[3]:
        return True
    if section[0] <= section[2] <= section[1]:
        return True
    if section[0] <= section[3] <= section[1]:
        return True
    return False

example_a = sum(map(is_subsection, [get_sections(a) for a in puzzle.example_data.splitlines()]))

assert(example_a == 2)

puzzle.answer_a = sum(map(is_subsection, [get_sections(a) for a in puzzle.input_data.splitlines()]))

example_b = sum(map(overlaps, [get_sections(a) for a in puzzle.example_data.splitlines()]))

assert(example_b == 4)

puzzle.answer_b = sum(map(overlaps, [get_sections(a) for a in puzzle.input_data.splitlines()]))

