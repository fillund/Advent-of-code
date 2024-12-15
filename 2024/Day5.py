from typing import Sequence
from aocd.models import Puzzle
import utils
from collections import defaultdict


def parse(data:str) -> tuple[dict[int,list[int]], list[list[int]]]:
    lines = data.splitlines()
    orderings = [tuple(utils.numbers(a)) for a in lines if '|' in a]
    updates = [utils.numbers(a) for a in lines if ',' in a]

    prerequisites = defaultdict(list)
    for a,b in orderings:
        prerequisites[b].append(a)

    return prerequisites, updates



def solve_a(data:str):
    prerequisites, updates = parse(data)
    correct_mids = []
    for update in updates:
        corrects = []
        for page in update:
            page_prereqs = prerequisites[page]
            page_is_correct = all([update.index(page) > update.index(other) for other in update if page!=other and other in page_prereqs])
            corrects.append(page_is_correct)
        if all(corrects):
            mid_index = len(update)//2
            correct_mids.append(update[mid_index])
    
    return sum(correct_mids)




    
def solve_b(data:str):
    pass
                


if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=5)

    example_a = solve_a(puzzle.example_data)
    assert (example_a == 143)
    answer_a = solve_a(puzzle.input_data)
    puzzle.answer_a = answer_a

    example_b = solve_b(puzzle.example_data)
    assert (example_b == 48)
    answer_b = solve_b(puzzle.input_data)
    puzzle.answer_b = answer_b
    