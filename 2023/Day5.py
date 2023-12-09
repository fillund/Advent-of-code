from aocd.models import Puzzle
import utils
import itertools as it
from tqdm import tqdm
import multiprocessing as mp
from functools import partial

def mapping(key:int, dst, src, length) -> int:
    offset = dst-src
    if src <= key < src+length:
        return key+offset
    else:
        return key

class Mapping():
    def __init__(self) -> None:
        self.mappings = {}

    def add_map(self, dst, src, length):
        offset = dst-src
        self.mappings[(src, src+length)] = lambda x: x+offset

    def map(self, key:int):
        for _range, _map in self.mappings.items():
            if _range[0] <= key < _range[1]:
                return _map(key)
        return key

# def calc_range(destination, source, length) -> tuple[list[int], list[int]]:
#     return list(range(source, source+length)), list(range(destination, destination+length))

def in_range(key, source, length) -> bool:
    return source<=key<source+length


    

def parse_data(data:str) -> tuple[list[int] , list[Mapping]]:
    mappings: list[Mapping] = []
    
    data_iter = iter(data.splitlines())

    seeds = utils.numbers(next(data_iter))

    for line in data_iter:
        if line == '':
            # mappings.append(dict())
            mappings.append(Mapping())
            next(data_iter) # skip mapping header
            continue
        
        dst_src_len = utils.numbers(line)
        # mappings[-1].update(dict(zip(*calc_range(*src_dst_len))))
        mappings[-1].add_map(*dst_src_len)
    
    return seeds, mappings

def chainmap(key, mappings:list[Mapping]) -> int:
    for mapping in mappings:
        key = mapping.map(key)
    return key

def solve_a(data:str) -> int:
    seeds, mappings = parse_data(data)

    return min(map(lambda x: chainmap(x, mappings), seeds))

def parse_seedrange(seed_range: list[int]):
    pairs = utils.grouper(seed_range, 2)
    assert len(pairs) == len(seed_range)/2
    return it.chain.from_iterable([range(pair[0], pair[0]+pair[1]) for pair in pairs])

def solve_b(data:str) -> int:
    seed_range, mappings = parse_data(data)

    seeds = parse_seedrange(seed_range)
    fun = lambda x: chainmap(x, mappings)
    return (min(map(fun, seeds)))

    

if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=5)

    example_a = solve_a(puzzle.example_data)
    assert (example_a == 35)
    puzzle.answer_a = solve_a(puzzle.input_data)

    example_b = solve_b(puzzle.example_data)
    assert(example_b == 46)
    puzzle.answer_b = solve_b(puzzle.input_data)