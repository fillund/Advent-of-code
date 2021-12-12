from os import path
from aocd.models import Puzzle
from typing import List, Dict, Tuple
from itertools import product
from collections import defaultdict

TEST_DATA="""fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""

TEST_DATA_SHORT = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""


def find_paths(trans:Dict[str, List[str]], start="start", goal="end", visited=set(), curr_path=[]) -> List[List[str]]:
    only_once = visited.copy()
    
    cp = curr_path.copy()
    cp.append(start)
    if start.islower():
        only_once.add(start)
    if start == goal: # Base case
        return [cp]
    paths = []
    for n in trans[start]:
        if n in only_once:
            continue

        for p in find_paths(trans, n, goal, only_once, cp):
            paths.append(p)
    return paths

def find_paths_b(trans:Dict[str, List[str]], start="start", goal="end", visited=defaultdict(int), curr_path=[]) -> List[List[str]]:
    only_twice = visited.copy()
    ONLY_ONCE = set(["start"])
    cp = curr_path.copy()
    cp.append(start)
    if start.islower():
        only_twice[start] += 1
    if start == goal: # Base case
        return [cp]
    paths = []
    for n in trans[start]:
        if n in ONLY_ONCE or only_twice[n] >= 1 and max(only_twice.values()) == 2:
            continue

        for p in find_paths_b(trans, n, goal, only_twice, cp):
            paths.append(p)
    return paths

def create_transitions(data:List[str]) -> Dict[str,List]:
    transitions = defaultdict(list)
    for line in data:
        a,b = line.split('-')
        transitions[a].append(b)
        transitions[b].append(a)
    return transitions


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=12)

    paths = find_paths(create_transitions(TEST_DATA_SHORT.splitlines()))
    assert(len(paths) == 10)

    paths = find_paths(create_transitions(puzzle.input_data.splitlines()))
    puzzle.answer_a = len(paths)

    paths = find_paths_b(create_transitions(TEST_DATA_SHORT.splitlines()))
    assert(len(paths) == 36)

    paths = find_paths_b(create_transitions(puzzle.input_data.splitlines()))
    puzzle.answer_b = len(paths)
    