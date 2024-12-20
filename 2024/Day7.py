from aocd.models import Puzzle
import utils
from operator import add, mul
from itertools import product


def num_concat(a:int,b:int) -> int:
    str_a = str(a)
    str_b = str(b)
    return int(str_a+str_b)

OPERATORS = [add, mul]
OPERATORS_B = [add, mul, num_concat]

def solve_a(data:str, operators=OPERATORS):
    total = 0
    for line in data.splitlines():
        numbers = utils.numbers(line)
        result = numbers[0]
        operands = numbers[1:]
        number_of_steps = len(operands)-1
        op_combinations = product(operators, repeat=number_of_steps)
        for op_combo in op_combinations:
            part_result = operands[0]
            for op, elem in zip(op_combo, operands[1:]):
                part_result = op(part_result, elem)
            if part_result == result:
                total += result
                break
    return total


            
        

    
def solve_b(data:str):
    return solve_a(data, OPERATORS_B)
                


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=7)

    example_a = solve_a(puzzle.example_data)
    assert (example_a == 3749)
    answer_a = solve_a(puzzle.input_data)
    puzzle.answer_a = answer_a

    example_b = solve_b(puzzle.example_data)
    assert (example_b == 11387)
    answer_b = solve_b(puzzle.input_data)
    puzzle.answer_b = answer_b
    