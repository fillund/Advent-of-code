from aocd.models import Puzzle
import utils
import math
import itertools as it

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

    col_widths = [0]*len(columns)
    for i, col in enumerate(columns):
        widths = [len(p) for p in col]
        col_widths[i] = max(widths)
        
    
    acc_widths = list(it.accumulate(col_widths))
    for i, line in enumerate(data.splitlines()):

        for j, cw in enumerate(col_widths):
            start = j + acc_widths[j] - cw # j for number of delimiters (spaces) passed, acc_widths for number of tokens passed
            stop = j + acc_widths[j]
            columns[j][i] = line[start:stop]


    return columns

def solve_a(data:str):
    cols = parse_columns(data)
    results: list[int] = []
    for col in cols:
        op = col[-1].strip()
        vals = [int(val) for val in col[:-1]]
        match op:
            case '+':
                results.append(sum(vals))
            case '*':
                results.append(math.prod(vals))
    return sum(results)

def num(s:str) -> int:
    try:
        return int(s)
    except ValueError:
        return 0 

def solve_b(data:str):
    cols = parse_columns(data)
    results = []
    for col in cols:
        op = col[-1].strip()

        raw = col[:-1]
        vals = []
        width = len(raw[0])
        for i in range(width):
            chars = [p[i] for p in raw]
            val = int(''.join(chars))
            vals.append(val)              

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
    