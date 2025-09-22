from aocd.models import Puzzle
import scipy.optimize
import numpy as np
from scipy.optimize import LinearConstraint
import utils
from dataclasses import dataclass
from itertools import product

@dataclass
class Machine():
    A : tuple[int,int]
    B: tuple[int,int]
    target: tuple[int,int]

COST_A = 3
COST_B = 1
B_TERM = 10000000000000

@dataclass
class Solution():
    A:int
    B:int
    cost:int

def parse_machines(data:str) -> list[Machine]:
    machines = []
    machines.append(Machine((0,0), (0,0), (0,0)))
    for line in data.splitlines():
        if line == '':
            machines.append(Machine((0,0), (0,0), (0,0)))
            continue
        if 'A' in line:
            machines[-1].A = tuple(utils.numbers(line))
        if 'B' in line:
            machines[-1].B = tuple(utils.numbers(line))
        if line.startswith('Prize'):
            machines[-1].target = tuple(utils.numbers(line))
    return machines

def find_solutions(m:Machine)->list[Solution]:
    solutions = []
    for a,b in product(range(0,101), repeat=2):
        if a*m.A[0] + b*m.B[0] == m.target[0] and a*m.A[1] + b*m.B[1] == m.target[1]:
            solutions.append(Solution(a, b, COST_A*a+COST_B*b))
    return solutions
            
def milp(m:Machine) -> Solution:
    c = [COST_A, COST_B]
    integrality = [1, 1] # Both integers
    bound = (m.target[0]+B_TERM, m.target[1]+B_TERM)
    constraints = [
        LinearConstraint(np.array([(m.A[0], m.B[0]), (m.A[1], m.B[1])]), lb=bound, ub=bound)
    ]
    options = {"time_limit": 10}
    res = scipy.optimize.milp(c, integrality=integrality, constraints=constraints, options=options)
    return res.fun if res.success else 0


def solve_a(data:str):
    machines = parse_machines(data)
    mins = []
    for m in machines:
        sol = find_solutions(m)
        if sol:
            mins.append(min(sol, key=lambda x: x.cost))
    return sum([m.cost for m in mins])
    
def solve_b(data:str):
    machines = parse_machines(data)
    sols = [milp(m) for m in machines]
    return sum(sols)
                


example_data = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=13)

    example_a = solve_a(example_data)
    assert (example_a == 480)
    answer_a = solve_a(puzzle.input_data)
    puzzle.answer_a = answer_a

    example_b = solve_b(example_data)
    # assert (example_b == 48)
    answer_b = solve_b(puzzle.input_data)
    puzzle.answer_b = answer_b
    