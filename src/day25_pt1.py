import networkx as nx
import numpy as np

from itertools import combinations


def parse_input(input_raw):
    lines = input_raw.strip().split('\n')

    parsed = {}
    for line in lines:
        component, connections = line.split(':')
        connections = connections.strip().split(' ')
        parsed[component] = connections

    return parsed


with open('inputs/day25.txt', 'r') as f:
    input_raw = f.read()

test_input_raw = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr"""


#connections = parse_input(test_input_raw)
connections = parse_input(input_raw)

g = nx.DiGraph()

for source, targets in connections.items():
    for target in targets:
        g.add_edge(source, target, weight=1)
        g.add_edge(target, source, weight=1)

for source, sink in combinations(g.nodes, 2):

    if source != sink:
        cut_value, (reachable, non_reachable) = nx.minimum_cut(g, source, sink, capacity='weight')

        # all weights are 1, so the cut value is the number of edges between the two sets
        if cut_value == 3:
            break 

result = len(reachable) * len(non_reachable)

# 562772
print(f"Part 1 solution is {result}")