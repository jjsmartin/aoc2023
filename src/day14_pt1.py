import numpy as np
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class Platform:
    round_rocks: np.ndarray
    cube_rocks: np.ndarray

    def __repr__(self):
        return f"Platform(round_rocks=\n{self.round_rocks}\n\ncube_rocks=\n{self.cube_rocks})"


def parse_input(raw_input):
    rows = np.array([list(line) for line in raw_input.splitlines()])

    round_rocks = np.where(rows == "O", 1, 0)
    cube_rocks = np.where(rows == "#", 1, 0)

    return Platform(round_rocks, cube_rocks)


def part1(platform):

    num_rows, num_cols = platform.round_rocks.shape
    column_loads = defaultdict(int)

    for col in range(num_rows):
        gap_count = 0
        for row in range(num_cols): 
            potential_load = num_rows - row
            
            if platform.round_rocks[row, col] == 1:
                load = potential_load + gap_count
                column_loads[col] += load

            elif platform.cube_rocks[row, col] == 1:
                gap_count = 0

            else:
                gap_count += 1

            #print(f"row={row}, col={col}, potential_load={potential_load}, actual_load={load}")
    #print()

    return sum(column_loads.values())


test_input_raw = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""


test_platform = parse_input(test_input_raw)
assert part1(test_platform) == 136

with open("inputs/day14.txt") as f:
    raw_input = f.read()
    platform = parse_input(raw_input)

result = part1(platform) # 102497
print(f"Part 1: {result}")