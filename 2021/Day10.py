from typing import Iterable, List
from aocd.models import Puzzle
from typing import List, Dict

PAIRS = {'(':')', '[':']', '{': '}', '<':'>'}
REVERSE_PAIRS = {v:k for k,v in PAIRS.items()}
SCORES = {')':3, ']':57, '}':1197, '>':25137}
B_SCORES =  {')':1, ']':2, '}':3, '>':4}
TEST_DATA = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""
B_TEST_DATA = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
(((({<>}<{<{<>}{[]{[]{}
{<[[]]>}<{[{[{[]{()[[[]
<{([{{}}[<[[[<>{}]]]>[]]"""

def solve_a(lines:List[str]):
    total = 0
    for line in lines:
        stack = []
        for char in line:
            if char in PAIRS.keys():
                stack.append(char)
            if char in REVERSE_PAIRS.keys():
                if REVERSE_PAIRS[char] != stack.pop():
                    total += SCORES[char]
    return total
    
def is_corrupt(line:str):
    stack = []
    for char in line:
        if char in PAIRS.keys():
            stack.append(char)
        if char in REVERSE_PAIRS.keys():
            if REVERSE_PAIRS[char] != stack.pop():
                return True
    return False

def solve_b(lines:List[str]):
    incomplete = [line for line in lines if not is_corrupt(line)]
    scores = []
    for line in incomplete:
        stack = []
        for char in line:
            if char in PAIRS.keys():
                stack.append(char)
            if char in REVERSE_PAIRS.keys():
                if REVERSE_PAIRS[char] != stack.pop():
                    assert(False)
        missing = [PAIRS[a] for a in reversed(stack)]
        line_score = calc_b_score(missing)
        scores.append(line_score)
    scores.sort()
    return scores[len(scores)//2]

def calc_b_score(chars:Iterable[str]):
    total = 0
    for char in chars:
        total *= 5
        total += B_SCORES[char]
    return total


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=10)
    lines = puzzle.input_data.splitlines()
    print(solve_a(["{([(<{}[<>[]}>{[]{[(<()>"]))
    assert(solve_a(TEST_DATA.splitlines()) == 26397)
    puzzle.answer_a = solve_a(lines)
    
    assert(calc_b_score("""}}]])})]""") == 288957)
    assert(calc_b_score("""}}>}>))))""") == 1480781)
    assert(solve_b(B_TEST_DATA.splitlines()) == 288957)

    puzzle.answer_b = solve_b(lines)