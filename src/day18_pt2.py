import numpy as np
from collections import namedtuple


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


def get_vertices(dig_plan):

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

    return vertices 


def get_border_length(dig_plan):

    return sum([instruction.distance for instruction in dig_plan])


def part2(input):

    dig_plan = parse_input(input) 
    vertices = get_vertices(dig_plan)
    border_length = get_border_length(dig_plan)
    capacity = shoelace(vertices) + border_length/2 + 1

    return int(capacity)


def shoelace(vertices):
    """Calculate the area of a polygon given its vertices."""
    n = len(vertices)-1
    return 0.5 * abs(sum([vertices[i][0] * vertices[(i+1)][1] - vertices[(i+1)][0] * vertices[i][1] for i in range(n)]))




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

assert part2(test_input) == 952408144115


with open("inputs/day18.txt") as f:
    input = f.read()

result = part2(input)

# 131431655002266
print(f"Part 2 result: {result}")