import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

from dataclasses import dataclass
from itertools import combinations


@dataclass
class Hailstone:
    px: int
    py: int
    pz: int
    vx: int
    vy: int
    vz: int

def parse_input(input_raw):
    hailstones = []
    for line in input_raw.split("\n"):
        position, velocity = line.split("@")
        position = position.split(",")
        velocity = velocity.split(",")

        hailstone = Hailstone(
            int(position[0]),
            int(position[1]),
            int(position[2]),
            int(velocity[0]),
            int(velocity[1]),
            int(velocity[2])
        )

        hailstones.append(hailstone)
    
    return hailstones


def get_intersection_times(a, b):

    t_a = sp.symbols('t_a')
    t_b = sp.symbols('t_b')
    
    eq1 = a.vx * t_a + a.px - b.vx * t_b - b.px
    eq2 = a.vy * t_a + a.py - b.vy * t_b - b.py

    solution = sp.solve([eq1, eq2], (t_a, t_b))
    return solution


test_input_raw = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""


with open("inputs/day24.txt", "r") as f:
    input_raw = f.read()

# hailstones = parse_input(test_input_raw)
# test_area_x = (7,27)
# test_area_y = (7,27)

hailstones = parse_input(input_raw)
test_area_x = (200000000000000,400000000000000)
test_area_y = (200000000000000,400000000000000)


intersection_times = {}
for i,j in combinations(range(len(hailstones)), 2):
    intersection_times[(i,j)] = get_intersection_times(hailstones[i], hailstones[j])

# limit to the test area and time >= 0
in_test_area = []
for (i,j), soln in intersection_times.items():

    if len(soln) == 0:
        continue

    t_a, t_b = list(soln.values())

    # check if the solution is in the past for either hailstone
    if t_a < 0 or t_b < 0:
        continue

    else:
        x = hailstones[i].vx * t_a + hailstones[i].px
        y = hailstones[i].vy * t_a + hailstones[i].py

        # check if the solution is in the test area
        if (test_area_x[0] <= x <= test_area_x[1]) and (test_area_y[0] <= y <= test_area_y[1]):
            in_test_area.append((i, j, x.evalf(), y.evalf()))


result = len(in_test_area)

# 15318
print(f"Part 1 result: {result} intersections in the test area") 
