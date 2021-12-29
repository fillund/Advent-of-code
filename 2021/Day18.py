import typing
from aocd.models import Puzzle
from typing import List, Dict, Optional, Tuple, Set, Union
from itertools import chain
import math
import functools as ft
from ast import literal_eval

TEST_DATA="""[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]""".splitlines()

def reduce(in_str: str) -> str:
    done = False
    current = in_str
    while not done:
        done = True
        depth = -1
        exploded = False
        for i, char in enumerate(current):
            if char == '[':
                depth += 1
                continue
            if char == ']':
                if depth >= 4: # Explode
                    new_str = explode(current, i)
                    exploded = True
                    current = new_str
                    done = False
                    break
                depth -= 1
                continue
        for i,char in enumerate(current):
            if exploded:
                break
            if char.isnumeric():
                num = int_win(current, i)
                if num >= 10:
                    current = split(current, i)
                    done = False
                    break
    assert(depth == -1)
    
    return current
                
                
            
def explode(in_str:str, pos:int) -> str:

    bracket_start = in_str.rfind('[', 0, pos)
    left, right = literal_eval(in_str[bracket_start+1: pos])
    is_leftmost = True
    for i in range(bracket_start, -1, -1):
        if in_str[i].isnumeric():
            num = int_win(in_str, i)
            is_leftmost = False
            break
    
    if is_leftmost:
        left_start = bracket_start
        num_replace_left = ''
    else:
        left_start = i
        num_replace_left = in_str[left_start:bracket_start].replace(str(num), str(num+left))

    is_rightmost = True
    for i in range(pos, len(in_str)):
        if in_str[i].isnumeric():
            num = int_win(in_str, i)
            is_rightmost = False
            break
    if is_rightmost:
        right_end = pos+1
        num_replace_right = ''
    else:
        right_end = i+1
        num_replace_right = in_str[pos+1:right_end].replace(str(num), str(num+right))
    # replace_mid = in_str[bracket_start:pos+1].replace(f'[{left},{right}]', '0')
    new_str = ''.join([in_str[:left_start], num_replace_left, '0', num_replace_right, in_str[right_end:]])
    return new_str

def split(in_str:str, pos:int)->str:
    num = int_win(in_str, pos)
    left = math.floor(num/2)
    right = math.ceil(num/2)
    rep_str = f"[{left},{right}]"
    new_str = ''.join([in_str[:pos-2], in_str[pos-2:pos+2].replace(str(num), rep_str), in_str[pos+2:]])
    return new_str

def add(a:str, b:str)->str:
    ans = reduce(f"[{a},{b}]")
    print(f"{a} + \n{b} =\n{ans}\n")
    return ans


# Returns the integer found in a +-1 window around pos
def int_win(in_str:str, pos:int) -> int:
    return int(''.join([c for c in in_str[pos-1:pos+2] if c.isnumeric()]))


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=18)

    assert(explode("[[1,2],3]", 5) == "[0,5]")
    assert(explode("[1,[2,3]]", 7) == "[3,0]")
    assert(explode("[[[[[9,8],1],2],3],4]", 8) == "[[[[0,9],2],3],4]")
    assert(explode("[[6,[5,[4,[3,2]]]],1]", 14) == "[[6,[5,[7,0]]],3]")

    assert(split("[[13,3],1]", 2) == "[[[6,7],3],1]")


    # assert(add("[[[[4,3],4],4],[7,[[8,4],9]]]", "[1,1]") == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")




#     test_sum = ft.reduce(add, """[1,1]
# [2,2]
# [3,3]
# [4,4]
# [5,5]
# [6,6]""".splitlines())
#     assert(test_sum == "[[[[5,0],[7,4]],[5,5]],[6,6]]")

    



    test_sum = ft.reduce(add, TEST_DATA)
    assert(test_sum == "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]")