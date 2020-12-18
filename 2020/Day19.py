# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

# %%
from aocd.models import Puzzle
from typing import Tuple, Dict
from collections import defaultdict
from itertools import combinations, product, count
from functools import lru_cache, reduce
from operator import mul
import re

puzzle = Puzzle(year=2020, day=19)
print(puzzle.input_data)


