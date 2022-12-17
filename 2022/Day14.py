import itertools as it
from aocd.models import Puzzle
from typing import List, Dict, Tuple, Set
from ast import literal_eval
from tqdm import tqdm

def candidates(x,y):
    return [(x, y+1), (x-1, y+1), (x+1, y+1)]

class Cavern:
    def __init__(self, input:str, b_cavern=False) -> None:
        self.rocks = set()
        self.sand = set()
        self.start_point = (500,0)
        self.b_cavern = b_cavern

        for line in input.splitlines():
            coords = [literal_eval(x) for x in line.split('->')]
            for a,b in it.pairwise(coords):
                self._create_line(a,b)

        self.deepest = max(self.rocks, key=lambda r: r[1])[1]
        self.occupied = self.rocks

        if b_cavern:
            self.floor_depth = self.deepest+2
            max_left = (self.start_point[0]-self.floor_depth, self.floor_depth)
            max_right = (self.start_point[0]+self.floor_depth, self.floor_depth)
            self._create_line(max_left, max_right)

    def _create_line(self, start:Tuple[int,int], end:Tuple[int,int]):
        xx = sorted([start[0], end[0]])
        yy = sorted([start[1], end[1]])
        for x, y in it.product(range(xx[0], xx[1]+1), range(yy[0], yy[1]+1)):
            self.rocks.add((x,y))
    
    def step(self):
        block = self.start_point


        depth_check = self.floor_depth if self.b_cavern else self.deepest

        while block[1] <= depth_check: # Make sure we dont follow the block into the abyss
            for block_cand in candidates(*block):
                if block_cand not in self.occupied:
                    block = block_cand
                    break # Break early if we can move
            else:
                #The loop ran through, we are now at rest
                self.sand.add(block)
                self.occupied.add(block)
                return block != self.start_point # Make sure we have actually moved
        # We have gone into the abyss. Stop
        return False
        
    def sim(self):
        while self.step():
            pass
        
    def count_sand(self):
        return len(self.sand)   
             


if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=14)

    ex_cavern = Cavern(puzzle.example_data)
    ex_cavern.sim()
    assert(ex_cavern.count_sand() == 24)

    cavern = Cavern(puzzle.input_data)
    cavern.sim()
    ans_a = cavern.count_sand()
    puzzle.answer_a = ans_a

    cavern_b = Cavern(puzzle.input_data, b_cavern=True)
    cavern_b.sim()
    ans_b = cavern_b.count_sand()
    puzzle.answer_b = ans_b
