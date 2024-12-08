from aocd.models import Puzzle
import utils





def solve_a(data:str):
    pass

    
def solve_b(data:str):
    pass
                


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=3)

    example_a = solve_a(puzzle.example_data)
    assert (example_a == 161)
    answer_a = solve_a(puzzle.input_data)
    puzzle.answer_a = answer_a

    example_b = solve_b(puzzle.example_data)
    assert (example_b == 48)
    answer_b = solve_b(puzzle.input_data)
    puzzle.answer_b = answer_b
    