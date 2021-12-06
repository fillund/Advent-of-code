from typing import List


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