from aocd.models import Puzzle
import utils
import math


def parse_columns(data:str) -> list[list[str]]:
    columns: list[list[str]] = []
    for line in data.splitlines():
        parts = line.split()
        if len(columns) == 0:
            for p in parts:
                columns.append([p])
        else:
            for c,p in zip(columns, parts):
                c.append(p)
    return columns

def solve_a(data:str):
    cols = parse_columns(data)
    results: list[int] = []
    for col in cols:
        op = col[-1]
        vals = [int(val) for val in col[:-1]]
        match op:
            case '+':
                results.append(sum(vals))
            case '*':
                results.append(math.prod(vals))
    return sum(results)

    
def solve_b(data:str):
    cols = parse_columns(data)
    results = []
    for col in cols:
        op = col[-1]
        max_width = max(len(p) for p in col[:-1])
        padded = [p.ljust(max_width) for p in col[:-1]] # TODO: Do not adjust. Must respect alignment in parsing
        vals = []
        for pos in range(max_width):
            chars = [p[pos] for p in padded]
            vals.append(int(''.join(chars)))

        match op:
            case '+':
                results.append(sum(vals))
            case '*':
                results.append(math.prod(vals))
    return sum(results)

                
example_data = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """

if __name__ == "__main__":
    puzzle = Puzzle(year=2025, day=6)

    example_a = solve_a(example_data)
    assert (example_a == 4277556)
    answer_a = solve_a(puzzle.input_data)
    puzzle.answer_a = answer_a

    example_b = solve_b(example_data)
    assert (example_b == 3263827)
    answer_b = solve_b(puzzle.input_data)
    puzzle.answer_b = answer_b
    