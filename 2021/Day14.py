from aocd.models import Puzzle
from typing import List, Dict, Tuple, Set
from collections import Counter, defaultdict
from itertools import tee

TEST_DATA = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def create_mapping(lines: List[str]):
    mapping = dict()
    for line in lines:
        a,b = line.split('->')
        mapping[a.strip()] = b.strip()
    return mapping

def polymerize(polymer_map: Dict[str, str], template:str) -> str:
    out_list = []
    for pair in pairwise(template):
        pair_str = ''.join(pair)
        if pair_str in polymer_map:
            out_list.append(''.join([pair_str[0], polymer_map[pair_str]]))
        else:
            out_list.append(pair_str[0])
    out_list.append(template[-1])
    return ''.join(out_list)

def most_and_least(in_str:str)-> Tuple[int, int]:
    c = Counter(in_str)
    commons = c.most_common()
    return (commons[0][1], commons[-1][1])

def solve(polymer_map, template, n):
    poly = poly_n(polymer_map, template, n)
    most, least = most_and_least(poly)
    return most-least

def poly_n(polymer_map, template, n):
    poly = template
    for i in range(n):
        poly = polymerize(polymer_map, poly)
    return poly


def solve_2(polymer_map: Dict[str,str], template, n):
    pair_counter = defaultdict(int)
    letter_counter = defaultdict(int)
    for c in template:
        letter_counter[c] += 1
    for pair in pairwise(template):
        pair_counter[''.join(pair)] += 1

    for i in range(n):
        pc_old = pair_counter.copy()
        
        for k  in pc_old.keys():
            
            new_char = polymer_map[k]
            p0 = ''.join([k[0], new_char])
            p1 = ''.join([new_char, k[1]])
            pair_counter[k] -= pc_old[k]
            pair_counter[p0] += pc_old[k]
            pair_counter[p1] += pc_old[k]
            letter_counter[new_char] += pc_old[k]
    return max(letter_counter.values())-min(letter_counter.values())


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=14)
    data = puzzle.input_data.splitlines()

    template = TEST_DATA.splitlines()[0]
    polymer_map = create_mapping(TEST_DATA.splitlines()[2:])
    ans = solve_2(polymer_map, template, 10)
    assert(ans == 1588)

    template = data[0]
    polymer_map = create_mapping(data[2:])
    ans = solve_2(polymer_map, template, 10)
    puzzle.answer_a = ans

    ans = solve_2(polymer_map, template, 40)
    puzzle.answer_b = ans
