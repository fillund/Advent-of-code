from enum import Enum
from aocd.models import Puzzle
import itertools as it
from typing import Dict, List, Sequence

puzzle = Puzzle(2022, 7)

class Kind(Enum):
    DIR = 0
    FILE = 1

TOTAL_SPACE = 70000000
NEEDED_SPACE = 30000000

class Node():
    def __init__(self, name:str, kind:Kind, size=None) -> None:
        self.name = name
        self.parent = None
        self.children : List[Node] = []
        self._size = size
        self.kind = kind

    def __iter__(self):
        yield self
        for child in list(it.chain.from_iterable(self.children)):
            yield child

    @property
    def is_dir(self):
        return self.kind == Kind.DIR

    def __repr__(self) -> str:
        return f'{self.name} {self.size} {self.children}'

    def get(self, name:str):
        if name == '..':
            return self.parent
        for c in self.children:
            if c.name == name:
                return c
        assert(False)

    @property
    def size(self):
        if (self._size is not None):
            return self._size
        self._size = sum([child.size for child in self.children])
        return self._size

    def add(self, new:'Node'):
        new.parent = self
        self.children.append(new)


def parser_a(data:Sequence[str]):
    start_node = Node('/', Kind.DIR)
    current_node = start_node

    for line in data:
        # We don't care about $ ls, since it doesn't add any info
        
        if line.startswith('$ cd'):
        # Change to new dir. Assume it exists in children
            dir_ = line[5:]
            current_node = current_node.get(dir_)
        elif line.startswith('dir'):
        # Add new dir
            dir_ = line[4:]
            current_node.add(Node(dir_, Kind.DIR))
        elif line[0].isdigit():
            val, name = line.split(' ')
            current_node.add(Node(name, Kind.FILE, int(val)))
    return start_node

example_data = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

node = parser_a(example_data.splitlines()[1:])

example_answer = sum(map(lambda x: x.size, filter(lambda x: x.is_dir and x.size <= 100000, node)))
assert(example_answer == 95437)

node_a = parser_a(puzzle.input_data.splitlines()[1:])
puzzle.answer_a = sum(map(lambda x: x.size, filter(lambda x: x.is_dir and x.size <= 100000, node_a)))

dirs_by_size = sorted(list(filter(lambda x: x.is_dir, node_a)), key=lambda x: x.size)
used_space = TOTAL_SPACE-node_a.size
answer_b = 0
for d in dirs_by_size:
    if used_space + d.size > NEEDED_SPACE:
        answer_b = d.size
        break

puzzle.answer_b = answer_b

