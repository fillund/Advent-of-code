from typing import DefaultDict, List
from aocd.models import Puzzle


TEST_DATA = """3,4,3,1,2"""
EXPECTED_1 = "2,3,2,0,1"
EXPECTED_2 = """1,2,1,6,0,8"""
EXPECTED_18 = """6,0,6,4,5,6,0,1,1,2,6,0,1,1,1,2,2,3,3,4,6,7,8,8,8,8"""


class LanternFish:
    def __init__(self, timer_init = 8) -> None:
        self.timer = timer_init

    def step(self):
        self.timer -= 1
        if self.timer < 0:
            self.timer = 6
            return True
        return False

class FishSchool:
    def __init__(self, fishes:List[LanternFish]) -> None:
        self.fishes = fishes

    def simulate_a(self, steps):
        for i in range(steps):
            new_fishes = []
            for fish in self.fishes:
                if fish.step():
                    new_fishes.append(LanternFish())
            self.fishes.extend(new_fishes)
        
    def get_total_fish(self):
        return len(self.fishes)
    
    def get_fish_state_str(self):
        string_state = [str(fish.timer) for fish in self.fishes]
        return ','.join(string_state)

class FishPool:
    def __init__(self, initial_timers) -> None:
        self.timer_dict = DefaultDict(int)
        for day in initial_timers:
            self.timer_dict[day] += 1

    def step(self):
        for i in range(-1, 8):
            self.timer_dict[i] = self.timer_dict[i+1]
        self.timer_dict[8] = self.timer_dict[-1]
        self.timer_dict[6] += self.timer_dict[-1]

    def simulate(self, steps):
        for i in range(steps):
            self.step()
    
    def get_total_fish(self):
        return sum([self.timer_dict[i] for i in range(9)])


if __name__ == "__main__":
    start_timers = [int(x) for x in TEST_DATA.split(',')]
    start_fishes = [LanternFish(x) for x in start_timers]
    school = FishSchool(start_fishes)
    school.simulate_a(1)
    assert(school.get_fish_state_str() == EXPECTED_1)
    school.simulate_a(1)
    assert(school.get_fish_state_str() == EXPECTED_2)
    school.simulate_a(16)
    assert(school.get_fish_state_str() == EXPECTED_18)
    print(school.get_fish_state_str())

    start_timers = [int(x) for x in open(file='2021\Day6.txt').read().split(',')]
    start_fishes = [LanternFish(x) for x in start_timers]
    school = FishSchool(start_fishes)
    school.simulate_a(80)
    print(f"Number of fish after 80 days: {school.get_total_fish()}")

    puzzle = Puzzle(year=2021, day=6)
    puzzle.answer_a = school.get_total_fish()
    # school.simulate_a(256-80)
    pool = FishPool(start_timers)
    pool.simulate(80)
    assert(pool.get_total_fish() == school.get_total_fish())
    pool.simulate(256-80)
    puzzle.answer_b = pool.get_total_fish()