from aocd.models import Puzzle
import re
from collections import defaultdict

def card_parse(line:str) -> tuple[set[int], set[int]]:
    _, rest = line.split(':')
    winning_str, have_str = rest.split('|')
    win_set = {int(num) for num in winning_str.split()}
    have_set = {int(num) for num in have_str.split()}
    return (win_set, have_set)

def score_game_a(win_set:set[int], have_set:set[int]) -> int:
    common = win_set.intersection(have_set)
    if len(common) > 0:
        return int(2**(len(common) - 1))
    else:
        return 0

def get_card_num(line:str) -> int:
    mo = re.search(r'\d+', line)
    assert mo
    return int(mo[0])       

def solve_a(data:str) -> int:
    return sum([score_game_a(*card_parse(line)) for line in data.splitlines()])

def solve_b(data:str) -> int:
    instances = defaultdict(int)
    for line in data.splitlines():
        card_id = get_card_num(line)
        instances[card_id] += 1 # Add original
        win_set, have_set = card_parse(line)
        matches = len(win_set.intersection(have_set))
        for i in range(card_id+1, card_id+matches+1):
            instances[i] += instances[card_id]
    return sum(instances.values())



if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=4)

    example_a = solve_a(puzzle.example_data)
    assert (example_a == 13)
    puzzle.answer_a = solve_a(puzzle.input_data)

    example_b = solve_b(puzzle.example_data)
    assert(example_b == 30)
    puzzle.answer_b = solve_b(puzzle.input_data)