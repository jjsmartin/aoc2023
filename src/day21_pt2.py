import math
import numpy as np
import pandas as pd
from collections import deque


class GardenMap:

    def __init__(self, raw_input):

        lines = raw_input.split("\n")
        lines = np.array([list(line) for line in lines])
        self.nrows, self.ncols = len(lines), len(lines[0])
        self.start = ((self.nrows-1)//2, (self.ncols-1)//2)
        self.plots = self.parse_input(raw_input)

    def parse_input(self, raw_input):
        lines = raw_input.split("\n")
        lines = np.array([list(line) for line in lines])
        nrows, ncols = len(lines), len(lines[0])

        garden_plots = np.ones((nrows, ncols), dtype=np.int8)
        garden_plots[lines == "."] = 0
        garden_plots[lines == "S"] = 0

        return garden_plots


def bfs_distance(grid, start):
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    rows, cols = len(grid), len(grid[0])

    distances = [[-1 for _ in range(cols)] for _ in range(rows)]
    
    # row, column, distance
    queue = deque([(start[0], start[1], 0)])
    
    while queue:
        r, c, dist = queue.popleft()

        # skip rocks, already visited or out of bounds
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == 1 or distances[r][c] != -1:
            continue
        
        distances[r][c] = dist
        
        for dr, dc in directions:
            queue.append((r + dr, c + dc, dist + 1))

    return np.array(distances)


class TiledGardenMap(GardenMap):

    def __init__(self, raw_input, N):

        super().__init__(raw_input)

        self.plots = np.tile(self.plots, (N, N))
        self.nrows, self.ncols = self.plots.shape
        self.start = ((self.nrows-1)//2, (self.ncols-1)//2)



with open("inputs/day21.txt") as f:
    input_raw = f.read()

# generate some data we can fit a polynomial to;
num_reachable_plots = []
num_tilings = [1,5,9]  # odd number of tilings, to match the puzzle
num_steps = []
for N in num_tilings:

    garden = TiledGardenMap(input_raw, N=N)
    target_steps = (garden.nrows - 1) // 2

    distances = bfs_distance(garden.plots, garden.start)

    # plots are reachable if:
    #  they are not rocks
    #  the distance is less than the target steps 
    #  the parity of the distance is the same as parity of the target steps
    reachable = (
        (distances >= 0) & \
        (distances <= target_steps) & \
        ((distances % 2) == (target_steps % 2))
    ) 

    num_reachable_plots.append(np.sum(reachable))
    num_steps.append(target_steps)

    
target_steps = 26501365
coefficients = np.polyfit(num_steps, num_reachable_plots, 2)
result = coefficients[0] * target_steps**2 + coefficients[1] * target_steps + coefficients[2]

# 616583483179597
print(f"Part 2 result: {result}")