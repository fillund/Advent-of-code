from aocd.models import Puzzle
import utils
import itertools as it
import more_itertools as mit

def invalid_id(num:int) -> bool:
    s = str(num)
    size = len(s)//2
    part_1 = s[:size]
    part_2 = s[size:]
    if part_1 == part_2:
        return True
    return False

def solve_a(data:str, filter_fun = invalid_id):
    ranges = data.split(',')
    invalid_ids = []
    for r in ranges:
        start, end = r.split('-')
        ra = range(int(start), int(end)+1, 1)
        ids = filter(filter_fun, ra)
        invalid_ids.extend(ids)
    return sum(invalid_ids)



    
def invalid_b(num:int) -> bool:
    s = str(num)
    max_size = len(s)//2
    for size in range(1, max_size+1):
        groups = utils.grouper(s, size)
        if ''.join(mit.collapse(groups)) != s:
            # The full string is not in groups
            continue
        if mit.all_equal(groups):
            return True
    return False

example_data = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""

if __name__ == "__main__":
    puzzle = Puzzle(year=2025, day=2)

    example_a = solve_a(example_data)
    assert (example_a == 1227775554)
    answer_a = solve_a(puzzle.input_data)
    puzzle.answer_a = answer_a

    example_b = solve_a(example_data, invalid_b)
    assert (example_b == 4174379265)
    answer_b = solve_a(puzzle.input_data, invalid_b)
    puzzle.answer_b = answer_b
    