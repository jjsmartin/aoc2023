import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

from dataclasses import dataclass

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


test_input_raw = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""


with open("inputs/day24.txt", "r") as f:
    input_raw = f.read()

#hailstones = parse_input(test_input_raw)
hailstones = parse_input(input_raw)

# find the position and velocity of a rock that intersects with 3 rocks
# 9 unknowns: 3 variables for the rock's velocity, 3 variables for the rock's position, 3 variables for the intersection times
px, py, pz, vx, vy, vz, t1, t2, t3 = sp.symbols('px, py, pz, vx, vy, vz, t1, t2, t3')

equations = [
    px + vx * t1 - hailstones[0].px - hailstones[0].vx * t1,
    py + vy * t1 - hailstones[0].py - hailstones[0].vy * t1,
    pz + vz * t1 - hailstones[0].pz - hailstones[0].vz * t1,

    px + vx * t2 - hailstones[1].px - hailstones[1].vx * t2,
    py + vy * t2 - hailstones[1].py - hailstones[1].vy * t2,
    pz + vz * t2 - hailstones[1].pz - hailstones[1].vz * t2,

    px + vx * t3 - hailstones[2].px - hailstones[2].vx * t3,
    py + vy * t3 - hailstones[2].py - hailstones[2].vy * t3,
    pz + vz * t3 - hailstones[2].pz - hailstones[2].vz * t3

]

solution = sp.solve(equations, px, py, pz, vx, vy, vz, t1, t2, t3)[0]

# sum of px, py, pz
result = solution[0] + solution[1] + solution[2]

# 870379016024859
print(f"Part 2 result: {result}")
