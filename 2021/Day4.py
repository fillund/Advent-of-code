from aocd.models import Puzzle
from typing import List, Dict
from collections import namedtuple

RowCol = namedtuple('RowCol', ['row', 'col'])


class Board:
    def __init__(self, rows: List[str]):
        self.rows = []
        for row in rows:
            temp_row = [int(elem) for elem in row.split()]
            self.rows.append(temp_row)
        self.marked : Dict[int,RowCol] = dict()
        self.is_bingoed = False
    
    def get_col(self, c:int) -> List[int]:
        col = []
        for row in self.rows:
            col.append(row[c])
        return col

    def mark(self, num: int):
        for r, row in enumerate(self.rows):
            for c, val in enumerate(row):
                if val == num:
                    self.marked[val] = RowCol(r, c)

    def has_bingo(self):
        if self.is_bingoed:
            return True
        width = len(self.rows[0])
        for r, row in enumerate(self.rows):
            is_marked = [x in self.marked for x in row]
            if all(is_marked):
                self.is_bingoed = True
                return True
        for c in range(width):
            col = self.get_col(c)
            is_marked = [x in self.marked for x in col]
            if all(is_marked):
                self.is_bingoed = True
                return True
        return False

    def get_unmarked_sum(self):
        total = 0
        for row in self.rows:
            for val in row:
                if not val in self.marked:
                    total += val
        return total





class Bingo:
    def __init__(self, numbers: List[int] ,boards: List[Board]):
        self.boards = boards
        self.numbers = numbers
    
    def play_until_first_win(self):
        for num in self.numbers:
            for board in boards:
                board.mark(num)
                if board.has_bingo():
                    return num*board.get_unmarked_sum()

    def play_until_last_win(self):
        bingoed_boards = set()
        for num in self.numbers:
            for b, board in enumerate(boards):
                if b in bingoed_boards:
                    continue
                board.mark(num)
                if board.has_bingo():
                    bingoed_boards.add(b)
                if len(bingoed_boards) == len(self.boards):
                    return board.get_unmarked_sum() * num

                    
        

def parse_blocks_to_boards(data: List[str]) -> List[Board]: 
    boards = []
    for line_num in range(len(data)):
        if data[line_num] == '':
            boards.append(Board(data[line_num+1:line_num+6]))
    return boards
        

if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=4)
    data = puzzle.input_data.splitlines()
    numbers = [int(x) for x in data[0].split(',')]
    boards = parse_blocks_to_boards(data)
    bingo = Bingo(numbers, boards)
    # result = bingo.play_until_first_win()
    result = bingo.play_until_last_win()
    print(result)
    # puzzle.answer_a = result
    puzzle.answer_b = result
    


                