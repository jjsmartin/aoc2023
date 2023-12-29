import networkx as nx
import numpy as np
from collections import namedtuple, deque

Instruction = namedtuple("Instruction", ["direction", "distance", "colour"])

def parse_input(raw):

    dig_plan = []
    for line in raw.split("\n"):
        parts = line.split(" ")

        direction = parts[0]
        distance = int(parts[1])
        colour = parts[2].replace("(", "").replace(")", "")

        instruction = Instruction(direction, distance, colour)
        dig_plan.append(instruction)

    return dig_plan


def form_grid(dig_plan):

    directions = {'U': (-1,0), 'D': (1,0), 'L': (0,-1), 'R': (0,1)}

    current_location = (0,0)
    grid_locations = []
    for instruction in dig_plan:
        di, dj = directions[instruction.direction]

        for i in range(instruction.distance):
            current_location = (current_location[0] + di, current_location[1] + dj)
            grid_locations.append(current_location)

    top_left = (min([location[0] for location in grid_locations]), min([location[1] for location in grid_locations]))
    bottom_right = (max([location[0] for location in grid_locations]), max([location[1] for location in grid_locations]))

    grid = np.zeros((bottom_right[0]-top_left[0]+1, bottom_right[1]-top_left[1]+1))
    for loc in grid_locations:
        grid[loc[0]-top_left[0]][loc[1]-top_left[1]] = 1

    return grid



test_input = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""

with open("inputs/day18.txt") as f:
    input = f.read()

dig_plan = parse_input(input)
#dig_plan = parse_input(test_input)


grid = form_grid(dig_plan)
G = nx.grid_2d_graph(grid.shape[0], grid.shape[1])

# remove edges that connect trenches to non-trenches
removed_edges = []
for (i_a, j_a), (i_b, j_b) in G.edges:
    if grid[i_a][j_a] != grid[i_b][j_b]:
        G.remove_edge((i_a, j_a), (i_b, j_b))
        removed_edges.append(((i_a, j_a), (i_b, j_b)))

# find the connected components: this will be the area enclosed by the trenches plus the exterior
connected_components = sorted(nx.connected_components(G), key=len, reverse=True)

# graph of the connected components
H = nx.Graph()

for i, component in enumerate(connected_components):
    H.add_node(i, members=component)

# which components were adjaced in the original graph?
for edge in removed_edges:
    for i, comp1 in enumerate(connected_components):
        for j, comp2 in enumerate(connected_components):
            if i < j:  # To avoid duplicate checks
                if (edge[0] in comp1 and edge[1] in comp2) or (edge[1] in comp1 and edge[0] in comp2):
                    H.add_edge(i, j)

interior_points = np.ones(grid.shape)
for component in connected_components[1:]:
    for i,j in component:
        interior_points[i][j] = 0

capacity = int(grid.sum() + interior_points.sum())

# 31171
print(f"Part 1 result: {capacity}")


# so we can see the grid
#np.savetxt("day18_grid.txt", grid, fmt="%d")
#np.savetxt("day18_interior.txt", interior_points, fmt="%d")


