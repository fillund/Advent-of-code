import typing
from aocd.models import Puzzle
from typing import List, Dict, Tuple, Set
from itertools import product
import numpy as np


def solve_a(Ty):
    return ((abs(Ty[0])-1) * (abs(Ty[0])) / 2 )

def passed_target(x, y, Tx, Ty):
    return x > Tx[1] or y < Ty[0]

def in_target(x,y, Tx, Ty):
    return Tx[0]<=x <= Tx[1] and Ty[0]<= y <= Ty[1]

def find_all(Tx, Ty):
    vx_max = Tx[1]+1
    # vx_min = sum(range(Tx[0]+1))  # Not correct, find if needed
    vy_max = abs(Ty[0])
    vy_min = min(Ty[0], -Ty[0])
    velocity_cand = list(product(range(vx_max+1), range(vy_min, vy_max+1)))
    print(f"Checking {len(velocity_cand)} number of candidates")
    valid_velocities = set()
    for v0 in velocity_cand:
        v = np.array(v0)
        pos = np.array([0,0])
        t = 0
        while not passed_target(*pos, Tx, Ty):
            pos += v
            if in_target(pos[0], pos[1], Tx, Ty):
                valid_velocities.add(v0)
                

            if v[0] != 0:
                v -= np.array([1, 0])
            v -= np.array([0, 1])

    print(f"Found {len(valid_velocities)} initial velocities.")
    return valid_velocities

        



def sum_m_to_n(m: int, n: int):
    return ((n-m+1)*(m+n))/2


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=17)
    Tx = (20, 30)
    Ty = (-10, -5)
    assert(solve_a(Ty) == 45)

    test_vels = find_all(Tx, Ty)
    assert(len(test_vels) == 112)





    Tx = (81, 129)
    Ty = (-150, -108)
    ans_a = solve_a(Ty)
    puzzle.answer_b = len(find_all(Tx, Ty))
