from enum import Enum
from aocd.models import Puzzle
import itertools as it
from typing import Dict, List, Sequence, Tuple
from utils import nwise

puzzle = Puzzle(2022, 10)

def parse_input(data:str):
    values = [1]
    cycles = [0]
    
    for line in data.splitlines():
        if line.startswith('addx'):
            val = int(line[5:])
            values.append(val)
            cycles.append(2)
        else:
            values.append(0)
            cycles.append(1)
    
    return list(zip(values, cycles))

def signal_strength(trace: List[Tuple[int, int]]):
    pairs = it.pairwise(trace) # Define here to keep the state in the inner loop
    signals = []
    for lim in range(20, 221, 40):
        for a,b in pairs:
            if b[1] >= lim:
                signals.append((a[0], lim))
                break
    print(signals)
    return sum(map(lambda x: x[0]*x[1], signals))

def create_trace(data):
    return list(it.accumulate(data,func=lambda x, y: (x[0]+y[0], x[1]+y[1])))


trace_ex = create_trace(parse_input(puzzle.example_data))

with open('2022\\10_long.txt', 'r') as f:
    trace_long = create_trace(parse_input(f.read()))

assert(signal_strength(trace_long) == 13140)

trace_a = create_trace(parse_input(puzzle.input_data))
answer_a = signal_strength(trace_a)
print(answer_a)
puzzle.answer_a = answer_a