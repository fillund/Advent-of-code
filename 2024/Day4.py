from aocd.models import Puzzle
import utils
from utils import Point
from collections import Counter



def cross_words(p:Point, grid:dict[Point, str], n=4):
    words = []
    dirs = []
    # Horizontal
    dirs.append(tuple([Point(p.x+i, p.y) for i in range(n)]))
    dirs.append(tuple([Point(p.x-i, p.y) for i in range(n)]))
    # Vertical
    dirs.append(tuple([Point(p.x, p.y+i) for i in range(n)]))
    dirs.append(tuple([Point(p.x, p.y-i) for i in range(n)]))
    # Diagonal
    dirs.append(tuple([Point(p.x+i, p.y+i) for i in range(n)]))
    dirs.append(tuple([Point(p.x+i, p.y-i) for i in range(n)]))
    dirs.append(tuple([Point(p.x-i, p.y+i) for i in range(n)]))
    dirs.append(tuple([Point(p.x-i, p.y-i) for i in range(n)]))

    for dir in dirs:
        word = ''.join([grid[pd] for pd in dir if pd in grid])
        words.append(word)
    return words

def x_words(p:Point, grid:dict[Point, str]):
    words = []
    dirs = []
    # Diagonal
    dirs.append(tuple([Point(p.x+i, p.y+i) for i in range(-1,2)]))
    dirs.append(tuple([Point(p.x+i, p.y-i) for i in range(-1,2)]))

    for dir in dirs:
        word = ''.join([grid[pd] for pd in dir if pd in grid])
        words.append(word)
    return words

def solve_a(data:str):
    grid = utils.parse_grid(data)
    xmases = 0
    for p in grid:
        word_count = Counter(cross_words(p, grid))
        xmases+= word_count["XMAS"]
    return xmases


    
def solve_b(data:str):
    grid = utils.parse_grid(data)
    xmases = 0
    for p in grid:
        if grid[p] != 'A':
            continue
        word_count = Counter(x_words(p, grid))
        if word_count["SAM"] + word_count["MAS"] == 2:
            xmases+=1
    
    return xmases           

example_data = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

if __name__ == "__main__":
    puzzle = Puzzle(year=2024, day=4)

    example_a = solve_a(example_data)
    assert (example_a == 18)
    answer_a = solve_a(puzzle.input_data)
    puzzle.answer_a = answer_a

    example_b = solve_b(example_data)
    assert (example_b == 9)
    answer_b = solve_b(puzzle.input_data)
    puzzle.answer_b = answer_b
    