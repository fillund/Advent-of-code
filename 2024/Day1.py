from aocd.models import Puzzle
import utils
from collections import Counter

def solve_a(data:str):
    num_rows = [utils.numbers(row) for row in data.splitlines()]
    col_1 = [a for a,b in num_rows]
    col_2 = [b for a,b in num_rows]
    sorted_zip = zip(sorted(col_1), sorted(col_2))
    differences = [abs(a-b) for a,b in sorted_zip]
    return sum(differences)

def solve_b(data:str):
    num_rows = [utils.numbers(row) for row in data.splitlines()]
    col_1 = [a for a,b in num_rows]
    col_2 = [b for a,b in num_rows]
    col_2_count = Counter(col_2)
    similarity_scores = [a * col_2_count[a] for a in col_1]
    return sum(similarity_scores)


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=1)

    example_a = solve_a(puzzle.example_data)
    assert (example_a == 11)
    answer_a = solve_a(puzzle.input_data)
    puzzle.answer_a = answer_a
    example_b = solve_b(puzzle.example_data)
    assert (example_b == 31)
    answer_b = solve_b(puzzle.input_data)
    puzzle.answer_b = answer_b
    
    