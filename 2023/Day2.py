from aocd.models import Puzzle
import re
from functools import reduce
from operator import mul

num_cubes = {'red':12, 'green':13, 'blue':14}

def is_possible(game:str, max_dict:dict[str,int]) -> bool:
    _,b = game.split(':')
    set_strings = b.split(';')
    for set_str in set_strings:
        parts = set_str.split(',')
        for part in parts:
            num_str = part.strip().split(' ')
            if int(num_str[0]) > max_dict[num_str[1]]:
                return False
    return True

def get_id(game:str) -> int:
    a,_ = game.split(':')
    game_id = int(a.split(' ')[-1])
    return game_id

def solve_a(data:str) -> int:
    lines = data.splitlines()
    return sum(map(get_id ,filter(lambda x: is_possible(x, num_cubes), lines)))
        
def cube_power(game:str) -> int:
    pattern = re.compile(r"(\d+) (blue|red|green)")            
    max_dict = dict.fromkeys(['green', 'red', 'blue'], 0)

    for match in pattern.findall(game):
        if int(match[0]) > max_dict[match[1]]:
            max_dict[match[1]] = int(match[0])
    
    return reduce(mul, max_dict.values())

def solve_b(data:str) -> int:
    lines = data.splitlines()
    return sum(map(cube_power, lines))

if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=2)

    example_a = solve_a(puzzle.example_data)
    assert (example_a == 8)
    puzzle.answer_a = solve_a(puzzle.input_data)

    example_b = solve_b(puzzle.example_data)
    assert(example_b == 2286)
    puzzle.answer_b = solve_b(puzzle.input_data)
