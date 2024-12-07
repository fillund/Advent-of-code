from aocd.models import Puzzle
import utils

def is_safe(report:list[int]):
    diffs = [b-a for a,b in utils.nwise(report, 2)]
    increasing = all([a>0 for a in diffs])
    decreasing = all([a<0 for a in diffs])
    small_steps = all(abs(a)<=3 for a in diffs)
    return (increasing or decreasing) and small_steps

def solve_a(data:str):
    reports = [utils.numbers(line) for line in data.splitlines()]
    safe_reports = [rep for rep in reports if is_safe(rep)]
    return len(safe_reports)

def solve_b(data:str):
    reports = [utils.numbers(line) for line in data.splitlines()]
    num_safe = 0
    for report in reports:
        if is_safe(report):
            num_safe+=1
            continue
        for i, level in enumerate(report):
            part_report = report.copy()
            del part_report[i]
            if is_safe(part_report):
                num_safe+=1
                break
    return num_safe


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=2)

    example_a = solve_a(puzzle.example_data)
    assert (example_a == 2)
    answer_a = solve_a(puzzle.input_data)
    puzzle.answer_a = answer_a

    example_b = solve_b(puzzle.example_data)
    assert (example_b == 4)
    answer_b = solve_b(puzzle.input_data)
    puzzle.answer_b = answer_b
    