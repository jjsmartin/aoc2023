import numpy as np
import re
import math 

from typing import List
from dataclasses import dataclass
from itertools import combinations

Pattern = np.array

def parse_input(raw):

    parts = raw.split("\n\n")
    patterns = []
    for part in parts:
        
        grid = [row.replace("#", "1").replace(".", "0")
                for row in part.split("\n")]

        patterns.append(Pattern([list(row) for row in grid], dtype=int))

    return patterns


def count_cols_left_of_vertical(pattern: Pattern) -> int:

    """Find the number of columns to the left of a line of vertical symmetry"""

    num_cols_left_of_vertical = None 

    indices = [(left_index, right_index) 
              for left_index, right_index in combinations(range(pattern.shape[1]+1), 2) 
              if (left_index == 0 or right_index == pattern.shape[1]) and (right_index - left_index > 1) and ((right_index - left_index) % 2 == 0)]

    indices = sorted(indices, key=lambda x: x[0] - x[1])  # we'll try the biggest subgrids first
    for left_index, right_index in indices:

        subgrid = pattern[:, left_index:right_index]

        # there should be exactly one difference between the subgrid and its flipped version
        left_half = subgrid[:, 0:subgrid.shape[1]//2]  # guaranteed to be even
        flipped = np.concatenate((left_half, np.fliplr(left_half)), axis=1)
        difference = np.subtract(subgrid, flipped) 
        num_differences = np.count_nonzero(difference)
        if num_differences == 1:
            num_cols_left_of_vertical = math.ceil((left_index + right_index) / 2)
            break 

    return num_cols_left_of_vertical
    


def count_rows_above_horizontal(pattern: Pattern) -> int:

    """Find the number of rows above a line of horizontal symmetry"""

    num_rows_above_horizontal = count_cols_left_of_vertical(pattern.T)

    return num_rows_above_horizontal



test_input_raw = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""

test_patterns = parse_input(test_input_raw)

with open("inputs/day13.txt") as f:
    raw = f.read()
    patterns = parse_input(raw)

def part2(patterns):
    result = 0
    for i, pattern in enumerate(patterns): 

        num_left_of_vertical = count_cols_left_of_vertical(pattern)
        num_above_horizontal = count_rows_above_horizontal(pattern)

        # seems from the wording that every pattern has exactly one line of symmetry
        if num_left_of_vertical is not None:
            print(f"Pattern {i} has a vertical line of symmetry: {num_left_of_vertical}")
            result += num_left_of_vertical

        if num_above_horizontal is not None:
            print(f"Pattern {i} has a horizontal line of symmetry: {num_above_horizontal}")
            result += (100 * num_above_horizontal)

    return result


assert part2(test_patterns) == 400
result = part2(patterns)
print(f"Part 2 test: {result}")  # 36755





