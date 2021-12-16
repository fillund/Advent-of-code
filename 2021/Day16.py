import itertools as it
import typing
from aocd.models import Puzzle
from typing import List, Dict, Tuple, Set
from collections import Counter, defaultdict
from enum import Enum, auto

TEST_HEXDATA = """D2FE28"""
TEST_HEXANS = """110100101111111000101000"""

class ParserState(Enum):
    HEADER = auto()
    LENGTH = auto()
    DATA = auto()

class PacketType(Enum):
    LITERAL = 4

class LengthType(Enum):
    TOTAL_LENGTH = 0
    SUBPACKETS = 1

class Packet:
    def __init__(self) -> None:
        pass

class LiteralPacket(Packet):
    def __init__(self) -> None:
        super().__init__()

class OperatorPacket(Packet):
    def __init__(self) -> None:
        super().__init__()

def bin2hex(hex_str:str)-> str:
    return format(int(hex_str, 16), 'b')


class Hexparser:
    def __init__(self, hexstr) -> None:
        self.bitstr = bin2hex(hexstr)
        self.state = ParserState.VERSION
        self.cursor = 0  # Cursors
        self.done = False
        self.decoded = []
        self.version_list = [] # For problem a


    def run(self):
        while self.cursor < len(self.bitstr):
            if self.state == ParserState.HEADER:
                version = self.bitstr[self.cursor:self.cursor+4]
                version = int(version, 2)
                self.cursor += 3
                type_ = self.bitstr[self.cursor:self.cursor+4]
                type_ = PacketType(int(type_, 2))
                self.cursor += 3
                self.version_list.append(version) 
                if type_ == PacketType.LITERAL:
                    self.state = ParserState.DATA

                else:
                    self.state = ParserState.LENGTH
                    
                    continue
                continue

            elif self.state == ParserState.DATA:
                lit = []
                lit_done = False
                while not lit_done:
                    byte = self.bitstr[self.cursor:self.cursor+6]
                    self.cursor += 5
                    lit_done = byte[0] == '0'
                    lit.append(byte[1:])
                value = int(''.join(lit), 2)
                self.state = ParserState.HEADER
            
            elif self.state == ParserState.LENGTH:
                lengthtype = LengthType(int(self.bitstr[self.cursor]))

# Do a recursive solution instead?
def parse(self):
        pass

                      
    


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=16)
    assert(bin2hex(TEST_HEXDATA) == TEST_HEXANS)