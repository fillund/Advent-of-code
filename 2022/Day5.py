from typing import List, Dict
from aocd.models import Puzzle
from collections import deque
from copy import deepcopy
import itertools as it
import re

LETTER = re.compile(r'([A-Z])')
NUMBER  = re.compile(r'(\d+)')

def numbers(x:str) -> List[int]:
    return [int(a[0]) for a in NUMBER.finditer(x)]

class Configuration():
    def __init__(self, stacks:Dict[int,deque]) -> None:
        self.stacks = deepcopy(stacks)

    def __str__(self):
        return str(self.stacks)

    def parse_header(data:str):
        header = list(it.takewhile(lambda x: x != '', data.splitlines()))
        positions = {int(a[0]):a.start() for a in NUMBER.finditer(header[-1])}
        pos2ind = {v:k for k,v in positions.items()}
        cols = {a:deque() for a in positions}
        for row in reversed(header[:-1]):
            for letter in LETTER.finditer(row):
                idx = pos2ind[int(letter.start())]
                cols[idx].append(letter[0])
        return Configuration(cols)


    def apply(self, q, f, t):
        new = Configuration(self.stacks)
        # print(f'move {q} from {f} to {t}')
        for _ in range(q):
            elem = new.stacks[f].pop()
            new.stacks[t].append(elem)
        return new

    def apply_inorder(self, q, f, t):
        new = Configuration(self.stacks)
        tq = deque()
        # print(f'move {q} from {f} to {t}')
        for _ in range(q):
            elem = new.stacks[f].pop()
            tq.append(elem)

        for _ in range(q):
            new.stacks[t].append(tq.pop())
        return new

    def top(self):
        return ''.join([self.stacks[k][-1] for k in self.stacks])

    def highest(self):
        return max([len(v) for _,v in self.stacks.items()])
if __name__ == "__main__":

    puzzle = Puzzle(year=2022, day=5)

    start = Configuration.parse_header(puzzle.example_data)

    lines = puzzle.example_data.splitlines()[start.highest()+2:]

    print(lines)

    conf = start
    for line in lines:
        conf = conf.apply(*numbers(line))

    example_a = conf.top()

    assert(example_a == 'CMZ')

    start = Configuration.parse_header(puzzle.input_data)
    lines = puzzle.input_data.splitlines()[start.highest()+2:]
    conf = start
    for line in lines:
        conf = conf.apply(*numbers(line))
    puzzle.answer_a = conf.top()

    conf = start
    for line in lines:
        conf = conf.apply_inorder(*numbers(line))
    puzzle.answer_b = conf.top()