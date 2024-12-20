from aocd.models import Puzzle
import utils
from collections import namedtuple

Chunk = namedtuple("Chunk", ["id", "size"])

def parse(data:str):
    diskmap = []
    id = 0
    for i, char in enumerate(data):
        if i % 2 == 0:
            new_part = [id] * int(char)
            id += 1
        else:
            new_part = [None] * int(char)
        diskmap.extend(new_part)
    return diskmap

def parse_file(data:str) -> list[Chunk]:
    diskmap:list[Chunk] = []
    id = 0
    for i, char in enumerate(data):
        if i % 2 == 0:
            chunk = Chunk(id, int(char))
            id += 1
        else:
            chunk = Chunk('.', int(char))
        diskmap.append(chunk)
    return diskmap

def solve_a(data:str):
    diskmap = parse(data)
    new_map = []
    for i, slot in enumerate(diskmap):
        if slot is not None:
            new_map.append(slot)
            continue
        for j, c in enumerate(reversed(diskmap[i:])):
            if c is not None:
                new_map.append(c)
                diskmap.pop(-j-1)
                break
    checksum = 0
    for i,val in enumerate(new_map):
        checksum += i*val
    return checksum

    
def solve_b(data:str):
    chunks = parse_file(data)
    has_moved = set()
    for j,chunk in enumerate(reversed(chunks)):
        if chunk.id != '.' and chunk not in has_moved:
            for i, c in enumerate(chunks):
                if c.id == '.' and c.size >= chunk.size and i<len(chunks)-j-1:
                    chunks[i] = Chunk(id='.', size=c.size-chunk.size)
                    chunks[chunks.index(chunk)] = Chunk(id='.', size=chunk.size)
                    chunks.insert(i, chunk)
                    has_moved.add(chunk)
                    break
    
    flat_map = []
    for chunk in chunks:
        new_part = [chunk.id] * chunk.size
        flat_map.extend(new_part)
    checksum = 0
    print("".join(map(str, flat_map)))
    for i,val in enumerate(flat_map):
        if val != ".":
            checksum += i*val
    return checksum


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=9)

    # example_a = solve_a(puzzle.example_data)
    # assert (example_a == 1928)
    # answer_a = solve_a(puzzle.input_data)
    # puzzle.answer_a = answer_a

    example_b = solve_b(puzzle.example_data)
    assert (example_b == 2858)
    answer_b = solve_b(puzzle.input_data)
    puzzle.answer_b = answer_b
    