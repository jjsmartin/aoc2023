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


def tilt(platform):

    num_rows, num_cols = platform.round_rocks.shape
    column_loads = defaultdict(int)

    new_round_rocks = np.zeros((num_rows, num_cols))  

    for col in range(num_rows):
        gap_count = 0
        for row in range(num_cols): 
            
            if platform.round_rocks[row, col] == 1:
                new_position = (row-gap_count, col)
                new_round_rocks[new_position] = 1

            elif platform.cube_rocks[row, col] == 1:
                gap_count = 0

            else:
                gap_count += 1

    return Platform(new_round_rocks, platform.cube_rocks)


def rotate(platform, k):

        rotated_round_rocks = np.rot90(platform.round_rocks, k=k)
        rotated_cube_rocks  = np.rot90(platform.cube_rocks, k=k)

        return Platform(rotated_round_rocks, rotated_cube_rocks)


def tilt_in_direction(platform, direction):

    """Rotate, tilt then rotate back, to mimic tilting in a particular direction."""

    # 90 degree rotation anticlockise puts west in the north position, and so on
    if direction == 'west':
        platform = rotate(platform, k=-1)
        platform = tilt(platform)
        platform = rotate(platform, k=1)

    elif direction == 'east':
        platform = rotate(platform, k=1)
        platform = tilt(platform)
        platform = rotate(platform, k=-1)

    elif direction == 'north':
        platform = tilt(platform)

    elif direction == 'south':
        platform = rotate(platform, k=2)
        platform = tilt(platform)
        platform = rotate(platform, k=2)

    else:
        raise ValueError(f"Invalid direction: {direction}")

    return platform


def column_loads(platform):

    num_rows, num_cols = platform.round_rocks.shape
    column_loads = defaultdict(int)

    for col in range(num_rows):
        for row in range(num_cols): 
            load = num_rows - row
            
            if platform.round_rocks[row, col] == 1:
                column_loads[col] += load

    return column_loads


def platform_to_hashable(platform):
    round_rocks = tuple(map(tuple, platform.round_rocks)) 
    cube_rocks = tuple(map(tuple, platform.cube_rocks))

    return (round_rocks, cube_rocks)

def hashable_to_platform(hashable):
    round_rocks, cube_rocks = hashable
    round_rocks = np.array(round_rocks)
    cube_rocks = np.array(cube_rocks)

    return Platform(round_rocks, cube_rocks)



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


with open("inputs/day14.txt") as f:
    raw_input = f.read()
    platform = parse_input(raw_input)

#platform = test_platform

#num_cycles = 1000000000
num_cycles = 1000

directions = ["north", "west", "south", "east"]




record = {}
for i in range(num_cycles):
    loads = column_loads(platform)
    print(f"Cycle {i}: {sum(loads.values())}")
    record[i] = sum(loads.values())
    
    for direction in directions:
        platform = tilt_in_direction(platform, direction)

    



loads = column_loads(platform)
result = sum(loads.values())
print(loads)

# 105008 obtained by running the above code for 1000 cycles and eyeballing it. Not clever, but it's late...
print(result)




