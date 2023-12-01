from aocd.models import Puzzle

def first_and_last(line: str) -> int:
    digits = list(filter(lambda x: x.isdigit(), line))
    return int(''.join([digits[0], digits[-1]]))

def solve_a(lines:list[str]) -> int:
    answer = sum(map(first_and_last, lines))
    return answer

mapping = {
    'one':'on1e',
    'two':'tw2o',
    'three':'thre3e',
    'four':'fou4r',
    'five':'fi5ve',
    'six':'si6x',
    'seven':'se7en',
    'eight':'eigh8t',
    'nine':'ni9ne'
}

# Insert proper digits inside word digits. Must keep starting/trailing characters to handle overlap
def text2digit(s:str) -> str:
    # Look for all digits
    t = s
    positions = {k:s.find(k) for k in mapping.keys()}

    while not all([pos == -1 for pos in positions.values()]):
        # Remove the first written digit
        valids = {k:v for k,v in positions.items() if v != -1}
        first = min(valids, key=valids.get)  # Pylance nags about this line, but it is fine
        s = s.replace(first, mapping[first], 1)
        positions = {k:s.find(k) for k in mapping.keys()}
    return s


def solve_b(lines:list[str]) -> int:
    return solve_a(list(map(text2digit, lines)))


if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=1)

    test_answer = solve_a(puzzle.example_data.splitlines())
    assert(test_answer == 142)
    answer_a = solve_a(puzzle.input_data.splitlines())
    puzzle.answer_a = answer_a

    test_answer_b = solve_b('''two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen'''.splitlines())
    assert(test_answer_b == 281)
    answer_b = solve_b(puzzle.input_data.splitlines())
    puzzle.answer_b = answer_b