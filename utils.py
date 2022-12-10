from typing import Sequence
from itertools import tee

def nwise(iterable:Sequence, n:int)->Sequence[tuple]:
    iters = tee(iterable, n)
    for i, iterator in enumerate(iters):
        for _ in range(i):
            next(iterator, None)
    return zip (*iters)

def grouper(iterable, n):
    "Return groups of n"
    args = [iter(iterable)]*n
    return list(zip(*args))