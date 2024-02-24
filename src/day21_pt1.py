import numpy as np
import networkx as nx

test_input_raw = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""


class GardenMap:

    def __init__(self, raw_input):

        lines = raw_input.split("\n")
        lines = np.array([list(line) for line in lines])

        self.nrows, self.ncols = len(lines), len(lines[0])
        self.start_pos = tuple(np.argwhere(lines == "S")[0])

        self.garden_plots = np.zeros((self.nrows, self.ncols), dtype=np.int8)
        self.garden_plots[lines == "."] = 1
        self.garden_plots[self.start_pos[0], self.start_pos[1]] = 1

        self.rocks = np.zeros((self.nrows, self.ncols), dtype=np.int8)
        self.rocks[lines == "#"] = 1

        self.g = None
        self.build_graph()
    
    def build_graph(self):

        self.g = nx.Graph()

        for row in range(self.nrows):
            for col in range(self.ncols):
                
                if self.rocks[row, col] == 1:
                    continue

                self.g.add_node((row, col))
                
                if col < self.ncols-1:
                    if self.garden_plots[row, col+1] == 1:
                        self.g.add_edge((row, col), (row, col+1))

                if row < self.nrows-1 :
                    if self.garden_plots[row+1, col] == 1:
                        self.g.add_edge((row, col), (row+1, col))


def count_reachable_plots(input_raw, target_steps):
    garden_map = GardenMap(input_raw)
    steps_to_nodes = nx.single_source_shortest_path_length(garden_map.g, garden_map.start_pos, cutoff=target_steps)
    reachable_nodes = {(row, col): nsteps
                      for (row, col), nsteps in steps_to_nodes.items()
                      if nsteps % 2 == 0}

    return len(reachable_nodes)


assert count_reachable_plots(test_input_raw, 6) == 16

with open("inputs/day21.txt") as f:
    input_raw = f.read()

target_steps = 64
result = count_reachable_plots(input_raw, target_steps=target_steps)

# 3716
print(f"There are {result} nodes reachable in {target_steps} steps")