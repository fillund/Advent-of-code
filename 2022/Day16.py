import itertools as it
from aocd.models import Puzzle
from typing import List, Dict, Tuple, Set
from tqdm import tqdm
from collections import namedtuple
import copy

Room = namedtuple('Room', ['name', 'rate', 'connections'])

class Flowsim:
    def __init__(self, rooms:Room, current_room = 'AA') -> None:
        self.rooms = rooms
        self.current_room = rooms[current_room]
        self.flow_rate = 0
        self.flow = 0
        self.opened_rooms = set()
        self.target_rooms = [name for name,room in self.rooms.items() if room.rate != 0]


    def step(self):
        self.flow += self.flow_rate
        return

    def branch(self):
        branches = []
        # Handle moving to new room
        if len(self.opened_rooms) != len(self.target_rooms):
            for new_room in self.current_room.connections:
                # if new_room not in self.opened_rooms:
                new_sim = copy.deepcopy(self)
                new_sim.current_room = self.rooms[new_room]
                # new_sim.opened_rooms.add(self.current_room.name) # Test
                branches.append(new_sim)
            # Handle opening current valve. Prune 0 flow_rate valves
            if self.current_room.name in self.target_rooms and self.current_room.name not in self.opened_rooms:
                self.flow_rate += self.current_room.rate
                self.opened_rooms.add(self.current_room.name)
                branches.append(self)
            # Handle NOP
        if len(branches) == 0:
            branches = [self]
        return branches



def get_rooms(input:str):
    rooms = {}
    for line in input.splitlines():
        name = line[6:8]
        rate = line[line.find('=')+1:line.find(';')]
        line2 = line.split(';')[1]
        others = line2[23:].strip().split(',')
        rooms[name] = Room(name, int(rate), [x.strip() for x in others])
    return rooms

# def calc_cost_to_go(rooms:List[Room]) -> Dict[str, Dict[str,int]]:
#     ctg = {}
#     for start in rooms:
#         visited = set()
        


def solve(rooms: List[Room]):
    sim = Flowsim(rooms)
    open_branches = [sim]
    for t in tqdm(range(30)):
        print(f'{t=} concurrent branches: {len(open_branches)}')
        new_branches = []
        for branch in open_branches:
            branch.step()
            new_branches.extend(branch.branch())
        if t > 7:
            new_branches = sorted(new_branches, key=lambda x: x.flow, reverse= True)[:1000]
        open_branches = new_branches
        
    return max([a.flow for a in open_branches])

        
    




if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=16)

    rooms = get_rooms(puzzle.example_data)

    # test_res = solve(rooms)
    # assert(test_res == 1651)

    rooms_a = get_rooms(puzzle.input_data)

    res_a = solve(rooms_a)
    print(f'res_a=')
    puzzle.answer_a = res_a