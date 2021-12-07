from aocd.models import Puzzle

def solve_a(positions):
    min_val = min(positions)
    max_val = max(positions)
    fuel_arr = []
    for i in range(min_val, max_val):
        temp_arr = [abs(pos-i) for pos in positions]
        fuel_arr.append(sum(temp_arr))
    return min(fuel_arr)

def solve_b(positions):
    min_val = min(positions)
    max_val = max(positions)
    fuel_arr = []
    for i in range(min_val, max_val):
        temp_arr = [b_cost(pos, i) for pos in positions]
        fuel_arr.append(sum(temp_arr))
    return min(fuel_arr)

def b_cost(pos, target):
    return sum(range(1, abs(pos-target)+1))
    




if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=7)
    positions = [int(x) for x in puzzle.input_data.split(',')]
    puzzle.answer_a = solve_a(positions)
    puzzle.answer_b = solve_b(positions)