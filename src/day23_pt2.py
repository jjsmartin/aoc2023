import networkx as nx
import numpy as np

from collections import defaultdict
from itertools import permutations


def parse_input_pt2(input_raw):
    trails = {}

    lines = input_raw.split("\n")
    nrows = len(lines)
    ncols = len(lines[0])

    for i, line in enumerate(lines):
        for j, val in enumerate(line):
            if val in [".", ">", "<", "^", "v"]:
                connections = [(i+1,j), (i-1,j), (i,j+1), (i,j-1)]
            elif val == "#":
                connections = None
            else:
                raise ValueError(f"Unknown character {val}")
        
            # only connect non-wall cells in range
            if connections is not None:
                trails[(i,j)] = [(row, col) 
                                for (row, col) in connections 
                                if 0 <= row < nrows and 0 <= col < ncols and lines[row][col] != "#"]

    g = nx.Graph(trails)

    # we start at the only path cell in the first row
    start = [pos for pos in trails if pos[0] == 0][0]

    # and end at the only path cell in the last row
    end = [pos for pos in trails if pos[0] == nrows-1][0]
            
    return start, end, g


test_input_raw = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""


with open("inputs/day23.txt", "r") as f:
    input_raw = f.read()

#start, end, g = parse_input_pt2(test_input_raw)
start, end, g = parse_input_pt2(input_raw)

lines = input_raw.split("\n")
#lines = test_input_raw.split("\n")
nrows = len(lines)
ncols = len(lines[0])

# identify nodes with more than 2 neighbours, plus the start and end nodes
junctions = [node for node in g.nodes if len(g[node]) > 2] + [start, end]

# remove all junction nodes from the graph
g_no_junctions = g.copy()
broken_edges = set()
for node in junctions:
    broken_edges.update(g.edges(node))
    g_no_junctions.remove_node(node)

# the connected components in what remains are the paths between the junctions
connected_components = [c for c in nx.connected_components(g_no_junctions)]

# create a reduced graph where each connected component is replaced by an edge
# the weight of the edge is the number of nodes in the connected component
g_reduced = g.copy()
for i in range(len(connected_components)):

    nodes_to_remove = connected_components[i]
    external_connections = {}

    for node in nodes_to_remove:
        for nbr in g_reduced.neighbors(node):
            if nbr not in nodes_to_remove:
                if node not in external_connections:
                    external_connections[node] = []
                external_connections[node].append(nbr)

    external_connections = [n for sublist in external_connections.values() for n in sublist]

    for node in connected_components[i]:
        g_reduced.remove_node(node)

    g_reduced.add_edge(external_connections[0], external_connections[1], weight=len(nodes_to_remove)+1)

# find all paths in the reduced graph
paths = list(nx.all_simple_paths(g_reduced, start, end))

path_lengths = [sum([g_reduced.get_edge_data(path[i], path[i+1])["weight"] 
                for i in range(len(path)-1)]) for path in paths]

longest_path_idx = np.argmax(path_lengths)
result = path_lengths[longest_path_idx]

# 6226
print(f"Part 2 result: {result}")