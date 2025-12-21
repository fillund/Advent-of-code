from aocd.models import Puzzle
import utils
import itertools as it

def lint(_list: list) -> int:
    s = [str(i) for i in _list]
    return int(''.join(s))

def max_remove(l:list[int]) -> list[int]:
    vals = []
    for p in range(len(l)):
        c = l.copy()
        c.pop(p)
        vals.append(c)
    return max(vals, key=lint)

def bank_joltage(bank:str, active_batteries=2) -> int:
    bank_int = [int(c) for c in bank]
    jolt_list = list(bank_int[-active_batteries:])
    rev_list = list(reversed(bank_int[:-active_batteries]))
    assert(len(rev_list)+len(jolt_list) == len(bank_int))
    for b in rev_list:
        if b >= jolt_list[0]:
            jolt_list.insert(0, b)
            jolt_list = max_remove(jolt_list)
    return lint(jolt_list)


def solve_a(data:str):
    banks = data.splitlines()
    joltages = [bank_joltage(b) for b in banks]
    return sum(joltages)


    
def solve_b(data:str):
    banks = data.splitlines()
    joltages = [bank_joltage(b, 12) for b in banks]
    return sum(joltages)
                
example_data = """987654321111111
811111111111119
234234234234278
818181911112111"""

if __name__ == "__main__":
    puzzle = Puzzle(year=2025, day=3)

    example_a = solve_a(example_data)
    assert (example_a == 357)
    answer_a = solve_a(puzzle.input_data)
    puzzle.answer_a = answer_a

    example_b = solve_b(example_data)
    assert (example_b == 3121910778619)
    answer_b = solve_b(puzzle.input_data)
    puzzle.answer_b = answer_b
    