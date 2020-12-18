# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from aocd.models import Puzzle
from typing import Tuple, Dict, List
from collections import defaultdict
from itertools import combinations, product, count, chain
from functools import lru_cache, reduce
from operator import mul, add
import re

puzzle = Puzzle(year=2020, day=18)
print(puzzle.input_data)


# %%
lines = [[x for x in line.replace('(', '( ').replace(')', ' )').split()] for line in puzzle.input_data.splitlines()]
test1 = '2 * 3 + (4 * 5)' # 26
test2 = '5 + (8 * 3 + 9 + 3 * 4 * 3)' # 437
test3 = '5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))' # 12240
test4 = '((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2' # 13632


# %%
class AST:
    operators = {'+': add, '*': mul}
    def __init__(self, rootValue, leftChild=None, rightChild=None):
        self.rootValue = rootValue
        self.leftChild = leftChild
        self.rightChild = rightChild

    def __str__(self):
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
            print(current)
            if token == '(':
                new = AST(None)
                current.leftChild = new
                stack.append(current)
                current = new
            elif token in AST.operators:
                current.rootValue = token
                new = AST(None)
                current.rightChild = new
                stack.append(current)
                current = new
            elif token.isnumeric():
                current.rootValue = int(token)
                current = stack.pop()
            elif token == ')':
                current = stack.pop()
            else:
                raise ValueError
        return root

# assert(create_AST(test1).evaluate() == 26)
# assert(create_AST(test2).evaluate() == 437)
# assert(create_AST(test3).evaluate() == 12240)
# assert(create_AST(test4).evaluate() == 13632)


# %%
def shunting_yard_ast(tokens:List[str]):
    # https://stackoverflow.com/questions/53839427/is-it-custumary-to-convert-from-infix-to-postfix-and-then-build-an-ast-on-math-e
    # https://www.reddit.com/r/learnprogramming/comments/3cybca/how_do_i_go_about_building_an_ast_from_an_infix/
    # https://en.wikipedia.org/wiki/Shunting-yard_algorithm
    output_stack = []
    op_stack = []
    operators = ['+', '*']
    
    def pop_op():
        op = op_stack.pop()
        if op == '(':
            return
        child1 = output_stack.pop()
        child2 = output_stack.pop()
        output_stack.append(AST(tok, child1, child2))

    for token in tokens:
        if token.isnumeric():
            output_stack.append(AST(int(token)))
        if token in operators:
            while len(op_stack > 0) and op_stack[-1] != '(':
                pop_op()
        if token == '(':
            op_stack.append(token)
        if token == ')':
            while op_stack[-1] != '(': # This will be a off by one error!
                pop_op()
                
re_par = re.compile(r'\(((\d|\*|\+|\s)+)\)')

def recursive_parse(expression:str) -> str:
    old_expression = expression
    if expression is None:
        raise ValueError
    while True:
        expression = re_par.sub(lambda x: recursive_parse(x.group(1)), expression)
        if expression == old_expression:
            break
        else:
            old_expression = expression
    idx = 0
    tokens = expression.split()
    acc = 0
    op = add
    while idx < len(tokens):
        if tokens[idx] == '+':
            op = add
        if tokens[idx] == '*':
            op = mul
        if tokens[idx].isnumeric():
            acc = op(acc, int(tokens[idx]))
        idx += 1
    return str(acc)

class CustInt(int):
    def __add__(self, a):
        return CustInt(super().__mul__(a))
    def __mul__(self, a):
        return CustInt(super().__add__(a))

def solve_b(puzzle_input):
    results = []
    for iline in puzzle_input:
        line = iline.replace(" ", "")
        line = line.replace('+', '.')
        line = line.replace('*', '+')
        line = line.replace('.', '*')
        tokens = []
        for token in line:
            if token not in '+*()':
                token = 'CustInt({})'.format(token)
            tokens.append(token)
        results.append(eval("".join(tokens)))
    return sum(results)


# %%
answer_a = sum([int(recursive_parse( '(' + x + ')' )) for x in puzzle.input_data.splitlines()])


# %%
puzzle.answer_a = answer_a


# %%
input_b = ['( ' + x.replace('*', ' )*( ') + ' )' for x in puzzle.input_data.splitlines()]


# %%
# assert(int(recursive_parse(test1)) == 46)
# assert(int(recursive_parse(test2)) == 1445)
# assert(int(recursive_parse(test3)) == 669060)
# assert(int(recursive_parse(test4)) == 23340)

# answer_b = sum([int(recursive_parse(x)) for x in input_b])
puzzle.answer_b = solve_b(puzzle.input_data.splitlines())


# %%
apa = re_par.sub(lambda x: recursive_parse(x.group(1)) ,'((72 * 103 + 6) + (1 + 2 + 3)) + 2 + 4 * 2')
print(apa)


