from posixpath import split
from aocd.models import Puzzle
from collections import defaultdict
from typing import Dict, Set, List

UNIQUE_SEGMENTS_DICT = {2 : 1, 3 : 7, 4 : 4, 7 : 8} # Number of segments => corresponding number
LENGTHS = {0:6, 1:2, 2:5, 3:5, 4:4, 5:5, 6:6, 7:3, 8:7, 9:6}
FIVERS = {2, 3, 5}
SIXERS = {0, 6, 9}

def solve_a(outputs_list: list):
    counter = defaultdict(int)
    for output in outputs_list:
        num_segments = len(output)
        if num_segments in UNIQUE_SEGMENTS_DICT:
            counter[num_segments] += 1
    return sum(counter.values())

def solve_display(display_list):
    char_dict = {}
    display_sets = [frozenset(x) for x in display_list]
    for disp in display_sets:
        if len(disp) in UNIQUE_SEGMENTS_DICT:
            char_dict[UNIQUE_SEGMENTS_DICT[len(disp)]] = disp 
    assert(set(char_dict.keys()) == {1, 4, 7, 8})
    while len(char_dict) != 10:
        for i in range(10):
            if i in char_dict:
                continue
            for disp in display_sets:
                if len(disp) == LENGTHS[3] and char_dict[1] < disp:
                    char_dict[3] = disp # 1 segments only occur in 3 out of the FIVERS
                
                elif len(disp) == LENGTHS[9] and char_dict[4] < disp:
                    char_dict[9] = disp # 4 segment only occur in 9 out of the sixers
                
                elif 9 in char_dict and len(disp) == LENGTHS[0] and char_dict[1] < disp:
                    char_dict[0] = disp
                
                elif {0, 9} < set(char_dict.keys()) and len(disp) == LENGTHS[6]:
                    char_dict[6] = disp

                elif 6 in char_dict and len(disp) == LENGTHS[5] and disp < char_dict[6]:
                    char_dict[5] = disp

                elif {3, 5} < set(char_dict.keys()) and len(disp) == LENGTHS[2] and disp < char_dict[8]:
                    char_dict[2] = disp
    return char_dict
                
def create_display_number(display_dict:Dict[int, Set[str]], outputs:List[str]):
    seg2num = {v:k for k,v in display_dict.items()}
    outputs_sets = [frozenset(x) for x in outputs]
    pairing = [seg2num[x] for x in outputs_sets]
    return 1000*pairing[0]+100*pairing[1]+10*pairing[2]+1*pairing[3]
              

def split_input(line:str):
    a,_,b = line.partition('|')
    return (a.split(), b.split())


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=8)
    lines = puzzle.input_data.splitlines()
    segments, outputs = [], []
    for line in lines:
        a, b = line.split('|')
        outputs.extend(b.split(' '))
    
    puzzle.answer_a = solve_a(outputs)

    total = 0
    for line in lines:
        a,b = split_input(line)
        total += create_display_number(solve_display(a), b)
    
    puzzle.answer_b = total