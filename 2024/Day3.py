from aocd.models import Puzzle
import utils
import re

PATTERN = r'mul\(\d{1,3},\d{1,3}\)'
PATTERN_B =  r"mul\(\d{1,3},\d{1,3}\)|do(?:n\'t)?\(\)"



def solve_a(data:str):
    matches = re.findall(PATTERN, data)
    muls = [utils.numbers(m) for m in matches]
    products = [a*b for a,b in muls]
    return sum(products)

    
def solve_b(data:str):
    matches = re.findall(PATTERN_B, data)
    muls = []
    enable = True
    for ma in matches:
        match ma:
            case "do()":
                enable = True
            case "don't()":
                enable = False
            case _ if enable:
                muls.append(utils.numbers(ma))
    products = [a*b for a,b in muls]
    return sum(products)
                


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=3)

    example_a = solve_a(puzzle.example_data)
    assert (example_a == 161)
    answer_a = solve_a(puzzle.input_data)
    puzzle.answer_a = answer_a

    example_b = solve_b("xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))")
    assert (example_b == 48)
    answer_b = solve_b(puzzle.input_data)
    puzzle.answer_b = answer_b
    