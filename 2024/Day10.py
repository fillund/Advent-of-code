from aocd.models import Puzzle
import utils




def solve_a(data:str):
    grid = utils.parse_grid(data)
    grid_num = {k:int(v) for k,v in grid.items()}
    trailheads = [k for k,v in grid_num.items() if v == 0]
    scores = []
    for head in trailheads:
        q = []
        score = 0
        scored: set[utils.Point] = set()
        q.extend([p for p in utils.cardinal_neighbours(head) if p in grid_num and grid_num[p] == grid_num[head]+1])
        while len(q) > 0:
            current = q.pop()
            q.extend([p for p in utils.cardinal_neighbours(current) if p in grid_num and grid_num[p] == grid_num[current]+1])
            if grid_num[current] == 9 and current not in scored:
                score += 1
                scored.add(current)
        scores.append(score)
    return sum(scores)

def solve_b(data:str):
    grid = utils.parse_grid(data)
    grid_num = {k:int(v) for k,v in grid.items()}
    trailheads = [k for k,v in grid_num.items() if v == 0]
    scores = []
    for head in trailheads:
        q = []
        score = 0
        q.extend([p for p in utils.cardinal_neighbours(head) if p in grid_num and grid_num[p] == grid_num[head]+1])
        while len(q) > 0:
            current = q.pop()
            q.extend([p for p in utils.cardinal_neighbours(current) if p in grid_num and grid_num[p] == grid_num[current]+1])
            if grid_num[current] == 9:
                score += 1
        scores.append(score)
    return sum(scores)
                
EXAMPLE_DATA = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=10)
    example_a = solve_a(EXAMPLE_DATA)
    assert (example_a == 36)
    answer_a = solve_a(puzzle.input_data)
    puzzle.answer_a = answer_a

    example_b = solve_b(EXAMPLE_DATA)
    assert (example_b == 81)
    answer_b = solve_b(puzzle.input_data)
    puzzle.answer_b = answer_b
    