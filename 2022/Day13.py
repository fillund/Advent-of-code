import itertools as it
from aocd.models import Puzzle
from typing import List, Dict, Tuple, Set
from ast import literal_eval
from operator import mul
from functools import reduce

class Pair:
    def __init__(self, first, second) -> None:
        self.first = first
        self.second = second

    @classmethod
    def from_str(cls, input:str):
        lines = input.splitlines()
        first = literal_eval(lines[0])
        second = literal_eval(lines[1])
        return cls(first, second)

    def __repr__(self) -> str:
        return f"Pair: {self.first} -- {self.second}"

    def in_order(self):
        for a,b in it.zip_longest(self.first, self.second):
            if b is None:
                return False
            if a is None:
                return True
            
            match a,b:
                case int(), int():
                    if a==b:
                        continue
                    return a<b
                case int(), list():
                    return Pair([a], b).in_order()
                case list(), int():
                    return Pair(a, [b]).in_order()
                case _:
                    result =  Pair(a, b).in_order()

            if result is not None:
                return result
        return None
        

class Packet:
    def __init__(self, cont, divider=False) -> None:
        self.cont = cont
        self.divider = divider

    @classmethod
    def from_str(cls, input:str) -> None:
        cont = literal_eval(input)
        return cls(cont)

    

    def __lt__(self, other):
        for a,b in it.zip_longest(self.cont, other.cont):
            if b is None:
                return False
            if a is None:
                return True
            
            match a,b:
                case int(), int():
                    if a==b:
                        continue
                    return a<b
                case int(), list():
                    return Pair([a], b).in_order()
                case list(), int():
                    return Pair(a, [b]).in_order()
                case _:
                    result =  Pair(a, b).in_order()

            if result is not None:
                return result
        return None



                
def part_a(pairs: List[Pair]) -> int:
    return sum([i for i, p in enumerate(pairs, start=1) if p.in_order()])
        
def part_b(packet_list: List[Packet]) -> int:
    return reduce(mul, [i for i,p in enumerate(sorted(packet_list), start=1) if p.divider])

if __name__ == "__main__":
    puzzle = Puzzle(year=2022, day=13)

    example_pairs = [Pair.from_str(x) for x in puzzle.example_data.split('\n\n')]
    print(example_pairs)

    for pair in example_pairs:
        if pair.in_order():
            assert(Packet(pair.first) < Packet(pair.second))

    print(part_a(example_pairs))
    assert(part_a(example_pairs) == 13)

    pairs_a = [Pair.from_str(x) for x in puzzle.input_data.split('\n\n')]

    ans_a = part_a(pairs_a)
    print(ans_a)
    puzzle.answer_a = ans_a
    
    for pair in pairs_a:

        assert(pair.in_order() == (Packet(pair.first) < Packet(pair.second)))

    ex_packet_list = [Packet.from_str(x) for x in puzzle.example_data.splitlines() if x!='']
    ex_packet_list.append(Packet([[2]], divider=True))
    ex_packet_list.append(Packet([[6]], divider=True))

    assert(part_b(ex_packet_list) == 140)

    packet_list = [Packet.from_str(x) for x in puzzle.input_data.splitlines() if x!='']
    packet_list.append(Packet([[2]], divider=True))
    packet_list.append(Packet([[6]], divider=True))
    ans_b = part_b(packet_list)
    puzzle.answer_b = ans_b