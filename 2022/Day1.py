from aocd.models import Puzzle

groups = []
group = []
puzzle = Puzzle(year=2022, day=1)
for line in puzzle.input_data.splitlines():
    if line == '':
        groups.append(group)
        group = []
        continue
    group.append(int(line))

sums = [sum(group) for group in groups]

puzzle.answer_a = max(sums)

puzzle.answer_b = sum(sorted(sums, reverse=True)[0:3])