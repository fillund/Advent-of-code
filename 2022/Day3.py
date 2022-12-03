from typing import List, Tuple
from aocd.models import Puzzle
import string

puzzle = Puzzle(year=2022, day=3)

prios = {letter:number for letter,number in zip(string.ascii_lowercase, range(1, 27))}
prios.update({letter:number for letter,number in zip(string.ascii_uppercase, range(27, 53))})

def grouper(iterable, n):
    "Return groups of n"
    args = [iter(iterable)]*n
    return list(zip(*args))


def get_sacks(data:str):
    lines = data.splitlines()
    return [(line[:len(line)//2], line[len(line)//2:]) for line in lines]

def get_overlap(sack:Tuple[str, str]):
    first_set = set(sack[0])
    sec_set = set(sack[1])
    overlap = first_set.intersection(sec_set)
    assert(len(overlap)==1)
    return overlap.pop()

def elf_overlap(sacks:List[Tuple[str, str]]):
    joined_sacks = [''.join(sack) for sack in sacks]
    left = set(joined_sacks[0])
    for sack in joined_sacks[1:]:
        left = left.intersection(set(sack))
    assert(len(left) == 1)
    return left.pop()

    

example_sacks = get_sacks(puzzle.example_data)
example_overlaps = map(get_overlap, example_sacks)
example_a = sum([prios[a] for a in example_overlaps])
assert(example_a == 157)

puzzle.answer_a = sum([prios[a] for a in map(get_overlap, get_sacks(puzzle.input_data))])

groups = grouper(get_sacks(puzzle.example_data), 3)


example_b = sum([prios[a] for a in map(elf_overlap, groups)])
assert(example_b == 70)

groups = grouper(get_sacks(puzzle.input_data), 3)
puzzle.answer_b = sum([prios[a] for a in map(elf_overlap, groups)])

