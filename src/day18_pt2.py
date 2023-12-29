import networkx as nx
import numpy as np
from collections import namedtuple, deque

Instruction = namedtuple("Instruction", ["direction", "distance"])

def parse_input(raw):

    dig_plan = []

    for line in raw.split("\n"):
        parts = line.split(" ")
        swapped_instruction = parts[2].replace("(", "").replace(")", "")
        distance, direction = correct_instruction(swapped_instruction)
        instruction = Instruction(direction, distance)
        dig_plan.append(instruction)

    return dig_plan


def correct_instruction(s: str) -> str:

    """Convert a line of the Part 2 dig plan to the Part 1 format."""

    # 0 means R, 1 means D, 2 means L, and 3 means U.
    directions = {0: "R", 1: "D", 2: "L", 3: "U"}

    distance_hex, direction = s[1:6], s[6]

    return int(distance_hex, 16), directions[int(direction)]


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


def shoelace(vertices):
    """Calculate the area of a polygon given its vertices."""
    n = len(vertices)
    return 0.5 * abs(sum([vertices[i][0] * vertices[(i+1)%n][1] - vertices[(i+1)%n][0] * vertices[i][1] for i in range(n)]))




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

# find the vertices
vertices = []
border_length = 0
i, j = 0, 0
for instruction in dig_plan:
    if instruction.direction == 'U':
        i -= instruction.distance
    elif instruction.direction == 'D':
        i += instruction.distance 
    elif instruction.direction == 'L':
        j -= instruction.distance
    elif instruction.direction == 'R':
        j += instruction.distance 
    else:
        raise ValueError("Unknown direction")

    vertices.append((i,j))
    border_length += instruction.distance

capacity = int(shoelace(vertices) + border_length/2 + 1)

# 131431655002266
print(f"Part 2 result: {capacity}")