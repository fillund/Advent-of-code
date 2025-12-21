from aocd.models import Puzzle
import utils
import itertools as it


def bank_joltage(bank:str, active_batteries=2) -> int:
    combs = it.combinations(bank, active_batteries)
    return max(map(lambda c: int(''.join(c)), combs))

def solve_a(data:str):
    banks = data.splitlines()
    return sum((bank_joltage(b) for b in banks))


    
def solve_b(data:str):
    
                
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
    