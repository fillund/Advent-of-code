from aocd.models import Puzzle
import itertools as it
from typing import Dict, List, Sequence, Tuple
import re
from dataclasses import dataclass
from tqdm import tqdm
import operator
from functools import reduce

puzzle = Puzzle(2022, 11)

NUMBER  = re.compile(r'(\d+)')

DIVISORS = [2, 3, 5, 7, 11, 13, 17, 19]
BIG_MOD = reduce(operator.mul, DIVISORS)

def numbers(x:str) -> List[int]:
    return [int(a[0]) for a in NUMBER.finditer(x)]

@dataclass
class Transaction:
    item:int
    target:int

class Monkey:
    def __init__(self, data:str, worry_divisor = 3) -> None:
        # Monkey 0:
        # Starting items: 53, 89, 62, 57, 74, 51, 83, 97
        # Operation: new = old * 3
        # Test: divisible by 13
        #     If true: throw to monkey 1
        #     If false: throw to monkey 5
        data = data.splitlines()
        self.items = numbers(data[1])
        _,self.op_expr = data[2].split('=')
        self.test_divisor = numbers(data[3])[0]
        self.true_target = numbers(data[4])[0]
        self.false_target = numbers(data[5])[0]
        self.worry_divisor = worry_divisor
        self.inspected_items = 0

    def add(self, item):
        self.items.append(item)

    def _calc_worry(self, old):
        # old used in op_expr, ex. new = old * 3
        new = eval(self.op_expr)
        new = new % BIG_MOD
        return new // self.worry_divisor

    def _test_worry(self, item):
        return item % self.test_divisor == 0

    def do_turn(self) -> List[Transaction]:
        transactions = []
        for item in self.items:
            self.inspected_items += 1
            new_worry = self._calc_worry(item)
            if self._test_worry(new_worry):
                trans = Transaction(new_worry, self.true_target)
            else:
                trans = Transaction(new_worry, self.false_target)
            transactions.append(trans)
        self.items = []
        return transactions

def monkey_factory(data:str):
    return [Monkey(part) for part in data.split('\n\n')]

def monkey_factory_b(data:str):
    return [Monkey(part, 1) for part in data.split('\n\n')]

def do_rounds(monkeys: List[Monkey], n:int) -> List[Monkey]:
    for i in tqdm(range(n)):
        for monkey in monkeys:
            transactions = monkey.do_turn()
            for trans in transactions:
                monkeys[trans.target].add(trans.item)
    return monkeys
        
def calc_monkey_business(monkeys: List[Monkey]):
    top = sorted(monkeys, key=lambda m: m.inspected_items, reverse=True)
    return top[0].inspected_items*top[1].inspected_items

example_monkeys = monkey_factory(puzzle.example_data)
example_monkeys = do_rounds(example_monkeys, 20)
example_answer = calc_monkey_business(example_monkeys)
assert(example_answer == 10605)

monkeys_a = monkey_factory(puzzle.input_data)
monkeys_a = do_rounds(monkeys_a, 20)
answer_a = calc_monkey_business(monkeys_a)
puzzle.answer_a = answer_a

monkeys_b = monkey_factory_b(puzzle.input_data)
monkeys_b = do_rounds(monkeys_b, 10000)
answer_b = calc_monkey_business(monkeys_b)
puzzle.answer_b = answer_b