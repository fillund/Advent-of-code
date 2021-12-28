import typing
from aocd.models import Puzzle
from typing import List, Dict, Optional, Tuple, Set, Union
from itertools import chain
import numpy as np
import math
from functools import reduce

ChildType = Optional[Union['SnailPair', int]]

TEST_DATA = """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]"""
FINAL_SUM = """[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"""

SMALL_TEST_DATA = """[[[[4,3],4],4],[7,[[8,4],9]]]
[1,1]"""
SMALL_TEST_SUM = """[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"""


class SnailPair:
    def __init__(self, left:ChildType, right:ChildType, parent:Optional['SnailPair'], depth=0) -> None:
        self.left = left
        self.right = right
        self.parent = parent
        self.depth = depth

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return f"[{repr(self.left)},{repr(self.right)}]"

    def __iter__(self):
        # ret_list = []
        if isinstance(self.left, SnailPair):
            # ret_list.append(self.left)
            for item in self.left:
                yield item
        yield self
        if isinstance(self.right, SnailPair):
            # ret_list.append(self.right)
            for item in self.right:
                yield item
        # return chain(*(map(iter, ret_list)), (self,))

    def add_to_depth(self, x):
        for n in self:
            try:
                n.depth += x
            except AttributeError:
                pass
        
    @classmethod
    def add(cls, x: 'SnailPair', y: 'SnailPair'):
        new_node = cls(x, y, None, depth=-1)
        new_node.left.parent = new_node
        new_node.right.parent = new_node
        new_node.add_to_depth(1)
        new_node.reduce()
        print(f"After addition {repr(new_node)}")
        return new_node

    def magnitude(self):
        try:
            left = self.left.magnitude()
        except AttributeError:
            left = int(self.left)
        try:
            right = self.right.magnitude()
        except AttributeError:
            right = int(self.right)
        return 3*left+2*right

    @classmethod
    def from_str(cls, in_str:str):
        curr_node = cls(None, None, None)
        nextleft = True
        depth = -1
        for char in in_str:
            if char == '[':
                depth += 1
                new_node = cls(None, None, None, depth)
                new_node.parent = curr_node
                if nextleft:
                    curr_node.left = new_node
                else:
                    curr_node.right = new_node
                curr_node = new_node
                nextleft = True
            elif char == ']':
                curr_node = curr_node.parent
                nextleft = True
                depth -= 1
            elif char == ',':
                nextleft = False
            else:
                if nextleft:
                    curr_node.left = int(char)
                else:
                    curr_node.right = int(char)
        curr_node.left.parent = None
        return curr_node.left

    def reduce(self):
        done = False
        while not done:
            done = True
            for n in self:
                # try:
                #     if isinstance(n.left, SnailPair) or isinstance(n.right, SnailPair):
                #         continue
                # except AttributeError:
                #     continue

                depth = n.depth
                if depth >= 4:
                    n.explode()
                    done = False
                    # print(f"After explosion: {repr(self)}")
                    break

                left = n.left
                right = n.right
                try:
                    if left >= 10:
                        new_left = math.floor(left/2)
                        new_right =  math.ceil(left/2)
                        new_node = self.__class__(new_left, new_right, n, depth+1)
                        n.left = new_node
                        # print(f"After split: {repr(self)}")
                        done = False

                        break
                except TypeError:
                    pass

                try:
                    if right >= 10:
                        new_left = math.floor(right/2)
                        new_right =  math.ceil(right/2)
                        new_node = self.__class__(new_left, new_right, n, depth+1)
                        n.right = new_node
                        # print(f"After split: {repr(self)}")
                        done = False
                        break
                except TypeError:
                    pass

                
    def explode(self):
        # print(f"{repr(self)}  is exploding")
        if self.parent.right is self:
            # print("I am the right child")
            try:
                prev = self.next_left() # I am the right child => Leftier elemet must exist
                prev.right += self.left
            except (AttributeError, TypeError):
                self.parent.left += self.left # The next element is in the parent

            next_node = self.next_right()
            if next_node.parent is None and next_node.right_most() is self: # I am the rightmost element, do nothing
                pass# next_node.right += self.right
            elif next_node.parent is None or isinstance(next_node.left, SnailPair):
                next_node.right += self.right # The next element is in the top
            else:
                next_node.left += self.right
                
            self.parent.right = 0 # Removes self

        elif self.parent.left is self:
            # print("I am the left child")
            prev = self.next_left()
            if prev.parent is None and prev.left_most() is self:
                pass
            elif prev.parent is None or isinstance(prev.right, SnailPair):
                prev.left += self.left
            else:
                prev.right += self.left
            
            try:
                next_node = self.next_right() # I am the left child => Rightier element must exist
                next_node.left += self.right
            except (AttributeError, TypeError):
                self.parent.right += self.right # The next element is in the parent

            self.parent.left = 0

    def next_right(self):
        curr_node = self.parent
        while curr_node.right_most() is self:
            if curr_node.parent is None:
                return curr_node # Check for none outside! Reached top => Either top is the next or I am the rightmost
            curr_node = curr_node.parent
        try:
            return curr_node.right.left_most()
        except AttributeError:
            return curr_node

    def next_left(self):
        curr_node = self.parent
        # Traverse upwards until forking, then go down
        while curr_node.left_most() is self:
            if curr_node.parent is None:
                return curr_node # Check for none outside!
            curr_node = curr_node.parent
        try:
            return curr_node.left.right_most()
        except AttributeError:
            return curr_node

    
    def right_most(self):
        curr_node = self
        while True:
            if isinstance(curr_node.right, SnailPair):
                curr_node = curr_node.right
            else:
                break
        return curr_node
    
    def left_most(self):
        curr_node = self
        while True:
            if isinstance(curr_node.left, SnailPair):
                curr_node = curr_node.left
            else:
                break
        return curr_node
        

if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=18)

    apa = SnailPair.from_str("[[1,2],3]")
    bepa = SnailPair.from_str("[1,[2,3]]")
    cepa = SnailPair.from_str("[[[[[9,8],1],2],3],4]")
    depa = SnailPair.from_str("[[[1,2],[3,4]],5]")
    epa = SnailPair.from_str("[[6,[5,[4,[3,2]]]],1]")
    
    # print(repr(apa))
    # print(repr(bepa))
    # print(repr(cepa))
    # print(repr(depa))
    # print(repr(epa))
    for i in epa:
        print(i, i.depth)
    # # epa.reduce()
    # print(repr(epa))
    


    test_terms = [SnailPair.from_str(s) for s in """[1,1]
[2,2]
[3,3]
[4,4]""".splitlines()]
    test_sum = reduce(SnailPair.add, test_terms)
    assert (repr(test_sum) == """[[[[1,1],[2,2]],[3,3]],[4,4]]""")

    test_terms = [SnailPair.from_str(s) for s in """[1,1]
[2,2]
[3,3]
[4,4]
[5,5]""".splitlines()]
    test_sum = reduce(SnailPair.add, test_terms)
    assert (repr(test_sum) == """[[[[3,0],[5,3]],[4,4]],[5,5]]""")

    test_terms = [SnailPair.from_str(s) for s in SMALL_TEST_DATA.splitlines()]
    test_sum = reduce(SnailPair.add, test_terms)
    assert (repr(test_sum) == SMALL_TEST_SUM)

    print()
    test_terms = [SnailPair.from_str(s) for s in TEST_DATA.splitlines()]
    test_sum = reduce(SnailPair.add, test_terms)
    # assert (repr(test_sum) == FINAL_SUM)

    print()
    test_terms = [SnailPair.from_str(s) for s in """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]""".splitlines()]
    test_sum = reduce(SnailPair.add, test_terms)
    # assert(str(test_sum) == "[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]")
    assert(test_sum.magnitude() == 4140)

    data = puzzle.input_data
    terms = [SnailPair.from_str(s) for s in data.splitlines()]
    snailsum = reduce(SnailPair.add, terms)
    # puzzle.answer_a = snailsum.magnitude()
    