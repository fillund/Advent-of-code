import itertools as it
import typing
from aocd.models import Puzzle
from typing import List, Dict, Tuple, Set
from collections import Counter, defaultdict
from enum import Enum, auto

TEST_HEXDATA = """D2FE28"""
TEST_HEXANS = """110100101111111000101000"""

TEST_DATA = """8A004A801A8002F478"""


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
    def __init__(self, version, typ, content) -> None:
        self.version = version
        self.typ = typ
        self.content = content

    def __str__(self) -> str:
        return ' '.join([str(self.version), str(self.typ), str(self.content)])

    def __repr__(self) -> str:
        return ' '.join([repr(self.version), repr(self.typ), repr(self.content)])
        



def hex2bin(hex_str:str)-> str:
    return ''.join([format(int(c, 16), '04b') for c in hex_str])


class Hexparser:
    def __init__(self, hexstr) -> None:
        self.bitstr = hex2bin(hexstr)
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
def parse(bitstr:str, num_packets = None) -> Tuple[list, str]:
    packets = []
    while len(bitstr) > 10:
        if num_packets is not None and len(packets)==num_packets:
            break

        version = int(bitstr[:3], 2)
        typ = int(bitstr[3:6], 2)

        if typ == PacketType.LITERAL.value:
            lit, bitstr = parse_literal(bitstr[6:])
            packets.append(Packet(version, typ, lit))
            
        
        else:
            lenghttype = int(bitstr[6])
            if lenghttype == LengthType.TOTAL_LENGTH.value:
                LEN_BITS = 7+15
                length = int(bitstr[7:LEN_BITS])

                packets.append(Packet(version, typ, None))
                new_packets, _ = parse(bitstr[LEN_BITS:LEN_BITS+length])
                bitstr = bitstr[LEN_BITS+length:]
                packets.extend(new_packets)

            elif lenghttype == LengthType.SUBPACKETS.value:
                LEN_BITS = 7+11
                n = int(bitstr[7:LEN_BITS], 2)
                packets.append(Packet(version, typ, None))
                new_packets, bitstr = parse(bitstr[LEN_BITS:], n)
                packets.extend(new_packets)

    return packets, bitstr



def parse_literal(bitstr:str) -> Tuple[int, str]:
    done = False
    lit = []
    i = 0
    while not done:
        byte = bitstr[i:i+5]
        i += 5
        done = byte[0] == '0'
        lit.append(byte[1:])
    value = int(''.join(lit), 2)                     
    return value, bitstr[i:]


if __name__ == "__main__":
    apa, bepa = parse("11101110000000001101010000001100100000100011000001100000")


    puzzle = Puzzle(year=2021, day=16)
    assert(hex2bin(TEST_HEXDATA) == TEST_HEXANS)

    bits = hex2bin(TEST_DATA)
    packets, remaining_bits = parse(bits)
    print(packets)
    print(remaining_bits)
    ver_sum = sum([p.version for p in packets])
    assert(ver_sum == 16)

    bits = hex2bin("620080001611562C8802118E34")
    packets, remaining_bits = parse(bits)
    print(packets)
    print(remaining_bits)
    ver_sum = sum([p.version for p in packets])
    assert(ver_sum == 12)

    bits = hex2bin("C0015000016115A2E0802F182340")
    packets, remaining_bits = parse(bits)
    print(packets)
    print(remaining_bits)
    ver_sum = sum([p.version for p in packets])
    assert(ver_sum == 23)

    bits = hex2bin("A0016C880162017C3686B18A3D4780")
    packets, remaining_bits = parse(bits)
    print(packets)
    print(remaining_bits)
    ver_sum = sum([p.version for p in packets])
    assert(ver_sum == 31)





    bits = hex2bin(puzzle.input_data)
    packets, remaining_bits = parse(bits)
    print(packets)
    print(remaining_bits)
    ver_sum = sum([p.version for p in packets])
    puzzle.answer_a = ver_sum
