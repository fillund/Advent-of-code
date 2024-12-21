from aocd.models import Puzzle
import utils
from collections import Counter
from tqdm import tqdm



def solve_a(data:str, num_blinks = 25):
    numbers = utils.numbers(data)
    counter = Counter(numbers)
    for _ in tqdm(range(num_blinks)):
        new_counter = Counter()
        for elem, count in counter.items():
            if elem == 0:
                new_counter[1] += count
            elif len(elem_str:=str(elem))%2 == 0:
                half = len(elem_str)//2
                a = int(elem_str[:half])
                b = int(elem_str[half:])
                new_counter[a] += count
                new_counter[b] += count
            else:
                new_counter[elem*2024] += count
        counter = new_counter
    return counter.total()
    
def solve_b(data:str):
    return solve_a(data, 75)
                
EXAMPLE = "125 17"

if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=11)

    example_a = solve_a(EXAMPLE)
    assert (example_a == 55312)
    answer_a = solve_a(puzzle.input_data)
    puzzle.answer_a = answer_a

    answer_b = solve_b(puzzle.input_data)
    puzzle.answer_b = answer_b
    