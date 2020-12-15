# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from aocd.models import Puzzle
from typing import Tuple, Dict
from collections import defaultdict
from itertools import combinations, product, count
from functools import lru_cache, reduce
from operator import mul
import re

puzzle = Puzzle(year=2020, day=14)
print(puzzle.input_data)


# %%
memory = {}
program = puzzle.input_data.splitlines()
program_pattern = r"(\w+)\[?(\d*)\]? = (\w+)"

def apply_mask(number:int, mask:str):
    number &= int(mask.replace('X', '1'), base=2)
    number |= int(mask.replace('X', '0'), base=2)
    return number

for line in program:
    match = re.match(program_pattern, line).groups()
    if match[0] == 'mask':
        mask = match[2]
    if match[0] == 'mem':
        memory[match[1]] = apply_mask(int(match[2]), mask)

answer_a = sum(memory.values())


# %%
puzzle.answer_a = answer_a


# %%
test1="""mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""



memory = {}
program = puzzle.input_data.splitlines()
# program = test1.splitlines()
program_pattern = r"(\w+)\[?(\d*)\]? = (\w+)"

def mask_address(address:int, mask:str) -> list:
    out = []
    num_floating = mask.count('X')
    xpos = [i for i,x in enumerate(mask) if x == 'X']
    ones = mask.replace('X', '0')
    address_temp = address|int(ones, base=2)
    add_str = bin(address_temp)[2:].rjust(36, '0')
    for comb in product('01', repeat=num_floating):
        temp_addr = add_str
        for i,pos in enumerate(xpos):
            temp_addr = temp_addr[:pos] + comb[i] + temp_addr[pos+1:]
        out.append(int(temp_addr, base=2))
    return out

for line in program:
    match = re.match(program_pattern, line).groups()
    if match[0] == 'mask':
        mask = match[2]
    if match[0] == 'mem':
        addresses = mask_address(int(match[1]), mask)
        for address in addresses:
            memory[address] = int(match[2])

answer_b = sum(memory.values())
print(answer_b)


# %%
puzzle.answer_b = answer_b


# %%
mask_address(10, '00X0')


# %%



