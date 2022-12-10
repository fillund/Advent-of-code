from enum import Enum
from aocd.models import Puzzle
import itertools as it
from typing import Dict, List, Sequence, Tuple

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

def complete_trace(data:str):
    # Returns register x value AFTER clk [0...]
    values = [1]
    for line in data.splitlines():
        if line.startswith('addx'):
            val = int(line[5:])
            values.append(values[-1])
            values.append(values[-1]+val)
        else:
            values.append(values[-1])
    return values

def signal_strength(trace: List[Tuple[int, int]]):
    pairs = it.pairwise(trace) # Define here to keep the state in the inner loop
    signals = []
    for lim in range(20, 221, 40):
        for a,b in pairs:
            if b[1] >= lim:
                signals.append((a[0], lim))
                break
    # print(signals)
    return sum(map(lambda x: x[0]*x[1], signals))

def print_crt(trace:List[int], fill_char='#', empty_char='.'):
    WIDTH = 40
    row = []
    for clk in range(1,241):
        during = clk-1
        screenpos = (clk-1)%WIDTH
        sprite = [trace[during]-1, trace[during], trace[during]+1]

        if screenpos in sprite:
            row.append(fill_char)
        else:
            row.append(empty_char)

        if clk % WIDTH == 0:
            print(''.join(row))
            row = []

    print('All printed, blip blop')       
        

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

with open('2022\\10_long.txt', 'r') as f:
    complete_example = complete_trace(f.read())

print(complete_example)
print_crt(complete_example)
complete_b = complete_trace(puzzle.input_data)
print_crt(complete_b, fill_char='#', empty_char=' ')