import networkx as nx
import numpy as np

def parse_input(input_raw):
    trails = {}

    lines = input_raw.split("\n")
    nrows = len(lines)
    ncols = len(lines[0])

    for i, line in enumerate(lines):
        for j, val in enumerate(line):
            if val == ".":
                connections = [(i+1,j), (i-1,j), (i,j+1), (i,j-1)]
            elif val == ">":
                 connections = [(i,j+1)]
            elif val == "<":
                connections = [(i,j-1)]
            elif val == "^":
                connections = [(i-1,j)]
            elif val == "v":
                connections = [(i+1,j)]
            elif val == "#":
                connections = None
            else:
                raise ValueError(f"Unknown character {val}")
        
            # only connect non-wall cells in range
            if connections is not None:
                trails[(i,j)] = [(row, col) 
                                for (row, col) in connections 
                                if 0 <= row < nrows and 0 <= col < ncols and lines[row][col] != "#"]

    g = nx.DiGraph(trails)

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

#start, end, g = parse_input(test_input_raw)
start, end, g = parse_input(input_raw)

all_paths = nx.all_simple_paths(g, start, end)

paths = []
path_lengths = []
for path in all_paths:
    paths.append(path)
    path_lengths.append(len(path)-1)  # dont count the start

longest_path_idx = np.argmax(path_lengths)
longest_path = paths[longest_path_idx]

result = path_lengths[longest_path_idx]

# 2202
print(f"Part 1 result: {result}")