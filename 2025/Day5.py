from aocd.models import Puzzle
import utils
import itertools as it


def parse_input(data:str) -> tuple[list[tuple[int,int]], list[int]]:
    # Return ranges, ids
    ranges: list[tuple[int,int]] = []
    ids: list[int] = []
    for line in data.splitlines():
        if not line:
            continue
        if "-" in line:
            start, stop = line.split("-")
            ranges.append((int(start), int(stop)))
        else:
            ids.append(int(line))
        
    return ranges, ids

def solve_a(data:str):
    ranges, ids = parse_input(data)
    count = 0
    for id in ids:
        for r in ranges:
            if r[0] <= id <= r[1]:
                count += 1
                break
    return count
    
def overlap(r1: tuple[int,int], r2:tuple[int,int]) -> bool:
    return r1[0] <= r2[0] <= r1[1] or r1[0] <= r2[1] <= r1[1]

def solve_b(data:str):
    ranges, _ = parse_input(data)
    merged_ranges: list[tuple[int,int]] = sorted(ranges, key=lambda x: x[0])
    while any([overlap(r1, r2) for r1,r2 in it.combinations(merged_ranges, 2)]):
        checked = set()
        new_merged = []
        for i, r in enumerate(merged_ranges):
            if r in checked:
                continue
            overlapping = [r]
            overlapping.extend([r2 for r2 in merged_ranges[i+1:] if overlap(r,r2)])
            checked |= set(overlapping)
            new_min = min([x[0] for x in overlapping])
            new_max = max([x[1] for x in overlapping])
            new_merged.append((new_min, new_max))
    
        merged_ranges = new_merged

    count = 0
    for mr in merged_ranges:
        count += mr[1]-mr[0]+1
    return count

                
example_data = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""

if __name__ == "__main__":
    puzzle = Puzzle(year=2025, day=5)

    example_a = solve_a(example_data)
    assert (example_a == 3)
    answer_a = solve_a(puzzle.input_data)
    puzzle.answer_a = answer_a

    example_b = solve_b(example_data)
    assert (example_b == 14)
    answer_b = solve_b(puzzle.input_data)
    puzzle.answer_b = answer_b
    