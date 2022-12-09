from enum import Enum
from aocd.models import Puzzle
import itertools as it
from typing import Dict, List, Sequence, Tuple
import numpy as np
from numpy.linalg import norm

puzzle = Puzzle(2022, 9)

example_data = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

def get_moves(data: str) -> List[Tuple[str, int]]:

    return [(move, int(amount)) for move, amount in map(lambda x: x.split(' '), data.splitlines())]

# print(get_moves(example_data))

class Rope:
    def __init__(self, num_knots:int) -> None:
        self.knots = [np.array((0,0)) for _ in range(num_knots)]
        self.visited = set([tuple(self.knots[-1])])
        self.history = [tuple(self.knots)]
    
    def __repr__(self) -> str:
        return f"Rope({self.knots}, {self.visited})"

    def move(self, dir, dist):
        vecs = Rope.dir2vecs(dir, dist)
        for vec in vecs:
            # self.print_state()
            # print(self.knots)
            self.knots[0] += vec

            for i, pair in enumerate(it.pairwise(self.knots)):
                head, tail = pair
                diff = head-tail

                if norm(diff, np.inf) > 1:
                    # The tail should move
                    tail += np.sign(diff)
                    self.knots[i+1] = tail
            self.history.append(tuple(self.knots))
            self.visited.add(tuple(self.knots[-1]))         

    def dir2vecs(dir: str, dist: int) -> List[np.array]:
        match dir:
            case 'D':
                base = np.array((0, -1))
            case 'U':
                base = np.array((0, 1))
            case 'L':
                base = np.array((-1, 0))
            case 'R':
                base = np.array((1, 0))
        return [base]*dist

    def num_visited(self):
        return len(self.visited)
            
    def print_state(self):
        maxx = 10#max(self.visited, key=lambda a: a[0])[0]
        minx = 0#min(self.visited, key=lambda a: a[0])[0]
        maxy = 10#max(self.visited, key=lambda a: a[1])[1]
        miny = 0#min(self.visited, key=lambda a: a[1])[1]
        for y in reversed(range(miny, maxy+2)):
            curr_line = []
            for x in range(minx, maxx+2):
                found = False
                for i, knot in enumerate(self.knots):
                    if not found and all((x,y) == knot):
                        curr_line.append(str(i))
                        found = True
                        break
                else:
                    curr_line.append('.')
            print(''.join(curr_line))
        print('-----------')

rope = Rope(2)

example_moves = get_moves(example_data)
# rope.print_state()
for move in example_moves:
    rope.move(*move)
    # rope.print_state()
    # print(rope.history)

print(rope.num_visited())
assert(rope.num_visited() == 13)

moves_a = get_moves(puzzle.input_data)
rope_a = Rope(2)
for move in moves_a:
    rope_a.move(*move)

answer_a = rope_a.num_visited()
assert(answer_a == 6464)
puzzle.answer_a = answer_a

example_b_rope = Rope(10)
for move in get_moves(example_data):
    example_b_rope.move(*move)
    example_b_rope.print_state()
example_b = example_b_rope.num_visited()
assert(example_b == 1)

larger_example = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""

example_b_rope = Rope(10)
for move in get_moves(larger_example):
    example_b_rope.move(*move)
    example_b_rope.print_state()
example_b = example_b_rope.num_visited()
assert(example_b == 36)

rope_b = Rope(10)
for move in moves_a:
    rope_b.move(*move)

puzzle.answer_b = rope_b.num_visited()