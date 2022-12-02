from aocd.models import Puzzle

puzzle = Puzzle(year=2022, day=2)

MAPPING = {'X':'A', 'Y':'B', 'Z':'C'}
SCORE_MAP = {'A':1, 'B':2, 'C':3}
SCORE_PAM = {v:k for k,v in SCORE_MAP.items()}
table = str.maketrans(MAPPING)

data = [a.translate(table).split(' ') for a in puzzle.input_data.splitlines()]

def score_outcome(elf, me):
    me_int = SCORE_MAP[me]
    elf_int = SCORE_MAP[elf]
    diff = me_int-elf_int
    if diff == 1 or diff == -2:
        return 6
    elif diff == 0:
        return 3
    else:
        return 0

    
def score_choice(elf, me):
    return SCORE_MAP[me]

def score_total(elf, me):
    return score_choice(elf, me) + score_outcome(elf, me)

# A=LOSE
# B=DRAW
# C=WIN
def choose(elf, outcome):
    elf_int = SCORE_MAP[elf]
    if outcome=='B':
        return elf
    elif outcome=='A':
        return SCORE_PAM.get(elf_int-1, 'C')
    else:
        return SCORE_PAM.get(elf_int+1, 'A')


assert(score_outcome('A', 'A') == 3)
assert(score_outcome('B', 'A') == 0)
assert(score_outcome('C', 'A') == 6)


answer_a = sum(map(lambda x: score_total(*x), data))
print(answer_a)
puzzle.answer_a = answer_a

answer_b = sum(map(lambda x: score_total(x[0], choose(*x)), data))
print(answer_b)
puzzle.answer_b = answer_b
