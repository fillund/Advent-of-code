# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %%
from aocd.models import Puzzle
from typing import Tuple, Dict
from collections import defaultdict
from itertools import combinations, product, count, chain
from functools import lru_cache, reduce
from operator import mul, add
import re

puzzle = Puzzle(year=2020, day=18)
# print(puzzle.input_data)


# %%
lines = [[x for x in line.replace('(', '( ').replace(')', ' )').split()] for line in puzzle.input_data.splitlines()]
test1 = '(2 * 3 + (4 * 5))'.replace('(', '( ').replace(')', ' )').split() # 26
test2 = '5 + (8 * 3 + 9 + 3 * 4 * 3)'.replace('(', '( ').replace(')', ' )').split() # 437
test3 = '5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))'.replace('(', '( ').replace(')', ' )').split() # 12240
test4 = '((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'.replace('(', '( ').replace(')', ' )').split() # 13632


# %%
class AST:
    operators = {'+': add, '*': mul}
    def __init__(self, rootValue, leftChild=None, rightChild=None):
        self.rootValue = rootValue
        self.leftChild = leftChild
        self.rightChild = rightChild

    def __repr__(self):
        return str((self.rootValue, self.leftChild, self.rightChild))

    def evaluate(self):
        if self.leftChild is None and self.rightChild is None:
            return self.rootValue
        elif self.rootValue in self.operators:
            return self.operators[self.rootValue](self.leftChild.evaluate(), self.rightChild.evaluate())
        else:
            raise ValueError
    

def create_AST(tokens:list):
        stack = []
        root = AST(None)
        current = root
        stack.append(root)
        for token in tokens:
            print(root)
            if token == '(':
                new = AST(None)
                current.leftChild = new
                stack.append(current)
                current = new
            elif token in AST.operators:
                current.rootValue = token
                new = AST(None)
                current.rightChild = new
                current = new
            elif token.isnumeric():
                new = AST(int(token))
                if current.leftChild is None:
                    current.leftChild = new 
                else:
                    current.rightChild = new              
            elif token == ')':
                current = stack.pop()
            else:
                raise ValueError
        return root

assert(create_AST(test1).evaluate() == 26)
assert(create_AST(test2).evaluate() == 437)
assert(create_AST(test3).evaluate() == 12240)
assert(create_AST(test4).evaluate() == 13632)


# %%
get_ipython().run_line_magic('debug', '')


