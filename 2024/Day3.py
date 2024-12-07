from aocd.models import Puzzle
import utils
import re

PATTERN = r'mul\(\d{1,3},\d{1,3}\)'
DO_PATTERN = r'do\(\)'
DONT_PATTERN = r"don't\(\)"


def solve_a(data:str):
    matches = re.findall(PATTERN, data)
    muls = [utils.numbers(m) for m in matches]
    products = [a*b for a,b in muls]
    return sum(products)

    
def solve_b(data:str):
    pass


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=3)

    example_a = solve_a(puzzle.example_data)
    assert (example_a == 161)
    answer_a = solve_a(puzzle.input_data)
    puzzle.answer_a = answer_a

    # example_b = solve_b(puzzle.example_data)
    # assert (example_b == 4)
    # answer_b = solve_b(puzzle.input_data)
    # puzzle.answer_b = answer_b
    