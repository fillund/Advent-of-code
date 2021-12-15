import itertools as it
from aocd.models import Puzzle
from typing import List, Dict, Tuple, Set
from collections import Counter, defaultdict
from math import inf, sqrt
from bisect import insort
import heapq as hq

TEST_DATA = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""
TEST_ANS = 40

TEST_DATA2 = """11637517422274862853338597396444961841755517295286
13813736722492484783351359589446246169155735727126
21365113283247622439435873354154698446526571955763
36949315694715142671582625378269373648937148475914
74634171118574528222968563933317967414442817852555
13191281372421239248353234135946434524615754563572
13599124212461123532357223464346833457545794456865
31254216394236532741534764385264587549637569865174
12931385212314249632342535174345364628545647573965
23119445813422155692453326671356443778246755488935
22748628533385973964449618417555172952866628316397
24924847833513595894462461691557357271266846838237
32476224394358733541546984465265719557637682166874
47151426715826253782693736489371484759148259586125
85745282229685639333179674144428178525553928963666
24212392483532341359464345246157545635726865674683
24611235323572234643468334575457944568656815567976
42365327415347643852645875496375698651748671976285
23142496323425351743453646285456475739656758684176
34221556924533266713564437782467554889357866599146
33859739644496184175551729528666283163977739427418
35135958944624616915573572712668468382377957949348
43587335415469844652657195576376821668748793277985
58262537826937364893714847591482595861259361697236
96856393331796741444281785255539289636664139174777
35323413594643452461575456357268656746837976785794
35722346434683345754579445686568155679767926678187
53476438526458754963756986517486719762859782187396
34253517434536462854564757396567586841767869795287
45332667135644377824675548893578665991468977611257
44961841755517295286662831639777394274188841538529
46246169155735727126684683823779579493488168151459
54698446526571955763768216687487932779859814388196
69373648937148475914825958612593616972361472718347
17967414442817852555392896366641391747775241285888
46434524615754563572686567468379767857948187896815
46833457545794456865681556797679266781878137789298
64587549637569865174867197628597821873961893298417
45364628545647573965675868417678697952878971816398
56443778246755488935786659914689776112579188722368
55172952866628316397773942741888415385299952649631
57357271266846838237795794934881681514599279262561
65719557637682166874879327798598143881961925499217
71484759148259586125936169723614727183472583829458
28178525553928963666413917477752412858886352396999
57545635726865674683797678579481878968159298917926
57944568656815567976792667818781377892989248891319
75698651748671976285978218739618932984172914319528
56475739656758684176786979528789718163989182927419
67554889357866599146897761125791887223681299833479"""
TEST_ANS2 = 315

class Graph:
    def __init__(self, lines:List[str]) -> None:
        nodes = {}
        for y, line in enumerate(lines):
            for x, risk in enumerate(line):
                nodes[(x,y)] = int(risk)
        self.width = max((a[0] for a in nodes.keys())) +1
        self.height = max((a[1] for a in nodes.keys())) +1
        self.corner = (self.width-1, self.height-1)
        transitions = self._create_trans(nodes)
        self.risks = nodes
        self.neighbours = transitions

    def _create_trans(self, nodes):
        transitions = defaultdict(list)
        for x,y in nodes.keys():
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                x2 = x+dx
                y2 = y+dy
                if 0<=x2<self.width and 0<=y2<self.height:
                    transitions[(x, y)].append((x2, y2))
        return transitions
    
    def expand(self):
        nodes = {}
        for i,j in it.product(range(5), range(5)):
            for k,v in self.risks.items():
                x = k[0]+i*self.width
                y = k[1]+j*self.height
                r = v + i + j
                if r>9:
                    r = r%10+1
                    
                nodes[(x,y)] = r
        self.width = max((a[0] for a in nodes.keys())) +1
        self.height = max((a[1] for a in nodes.keys())) +1
        self.corner = (self.width-1, self.height-1)
        transitions = self._create_trans(nodes)
        self.risks = nodes
        self.neighbours = transitions


    def plot_path(self, path):
        out = []
        for y in range(self.corner[1]+1):
            for x in range(self.corner[0]+1):
                if (x,y) in path:
                    out.append(str(self.risks[(x,y)]))
                else:
                    out.append('.')
            out.append('\n')
        with open(str(self.width), 'w') as f:
            f.write(''.join(out))

    def __str__(self):
        out = []
        for y in range(self.corner[1]+1):
            for x in range(self.corner[0]+1):
                out.append(str(self.risks[(x,y)]))
            out.append('\n')
        return ''.join(out).rstrip()

def heuristic(p1, p2):
    return sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
    # return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

def shortest_path(g:Graph, start:Tuple[int, int], target:Tuple[int, int]):

    q = [(0, start)]
    dist = {k:inf for k in g.risks.keys()} # The actual distance
    visited = set()
    # score = {k:inf for k in g.risks.keys()}
    # score[start] = heuristic(start, target) # The one to sort by
    dist[start] = 0
    prev = {}
    while q:
        # r, u = q.pop(0)
        r, u = hq.heappop(q)
        visited.add(u)
        # if u == target:
        #     break

        for v in g.neighbours[u]:
            alt = r + g.risks[v]
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                # score[v] = alt + heuristic(v, target)
                if v not in visited:
                    hq.heappush(q, (dist[v], v))
    path = recreate_path(prev, target)
    # print(path)
    # print([g.risks[k] for k in path])
    g.plot_path(path)
    return dist[target]

def recreate_path(cameFrom:dict, target):
    path = [target]
    current = target
    while current in cameFrom:
        current = cameFrom[current]
        path.insert(0, current)
    return path



if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=15)
    g = Graph(TEST_DATA.splitlines())
    ans = shortest_path(g, (0,0), g.corner)
    assert(ans == TEST_ANS)

    g = Graph(puzzle.input_data.splitlines())
    ans = shortest_path(g, (0,0), g.corner)
    puzzle.answer_a = ans

    g2 = Graph(TEST_DATA.splitlines())
    g2.expand()
    assert(str(g2) == TEST_DATA2)
    ans = shortest_path(g2, (0,0), g2.corner)
    assert(ans == TEST_ANS2)

    g.expand()
    ans = shortest_path(g, (0,0), g.corner)
    puzzle.answer_b = ans
    