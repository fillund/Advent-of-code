from aocd.models import Puzzle
import utils
import math




def solve_a(data:str):
    value = 50
    values = [value]
    for line in data.splitlines():
        dir, val = line[0], int(line[1:])
        match dir:
            case 'R': values.append(int(math.fmod(values[-1]+val, 100)))
            case 'L': values.append(int(math.fmod(values[-1]-val, 100)))
    return len(list(filter(lambda x: x==0, values)))
 
    
def solve_b(data:str):
    running = 50
    count = 0
    for line in data.splitlines():
        dir, val = line[0], int(line[1:])
        match dir:
            case 'R': 
                for _ in range(val):
                    running += 1
                    if running == 100:
                        running -= 100
                    if running == 0:
                        count += 1
            case 'L': 
                for _ in range(val):
                    running -=1
                    if running == 0:
                        count += 1
                    if running == -1:
                        running += 100
    return count


                
example_data = """L68
L30
R48
L5
R60
L55
L1
L99
R14 
L82"""

if __name__ == "__main__":
    puzzle = Puzzle(year=2025, day=1)

    example_a = solve_a(example_data)
    assert (example_a == 3)
    answer_a = solve_a(puzzle.input_data)
    puzzle.answer_a = answer_a

    example_b = solve_b(example_data)
    assert (example_b == 6)
    answer_b = solve_b(puzzle.input_data)
    puzzle.answer_b = answer_b
    