from aocd.models import Puzzle
from collections import Counter
from typing import List

puzzle = Puzzle(year=2021, day=3)

data = puzzle.input_data.splitlines()

def solution1(inputs: List[str]):
    num_bits = len(inputs[0])
    common_string = ''
    for bit_pos in range(num_bits):
        posx = [bits[bit_pos] for bits in inputs]
        counter = Counter(posx)
        common_string = common_string + counter.most_common(1)[0][0]
    gamma = int(common_string, 2) % 2**num_bits
    epsilon = (~gamma) & (2**num_bits - 1)
    return gamma*epsilon

def solution2(inputs: List[str]):
    num_bits = len(inputs[0])
    candidates = inputs
    goal_string = ''
    for bit_pos in range(num_bits):
        posx = [bits[bit_pos] for bits in candidates]
        counter = Counter(posx)
        if counter['1'] >= counter['0']:
            goal_string += '1'
        else:
            goal_string += '0'
        # goal_string += counter.most_common()[0][0]
        candidates = [elem for elem in candidates if elem.startswith(goal_string)]
        if len(candidates) == 1:
            break
    oxygen = int(candidates[0], 2) % 2**num_bits
    candidates = inputs
    goal_string = ''
    for bit_pos in range(num_bits):
        posx = [bits[bit_pos] for bits in candidates]
        counter = Counter(posx)
        if counter['0'] <= counter['1']:
            goal_string += '0'
        else:
            goal_string += '1'
        # goal_string += counter.most_common()[-1][0]
        candidates = [elem for elem in candidates if elem.startswith(goal_string)]
        if len(candidates) == 1:
            break
    scrubber = int(candidates[0], 2) % 2**num_bits

    return oxygen*scrubber



# ans = solution1(data)
puzzle.answer_a = solution1(data)
puzzle.answer_b = solution2(data)