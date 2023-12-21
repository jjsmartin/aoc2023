import numpy as np

from dataclasses import dataclass
from typing import Dict
from scipy.spatial.distance import cdist


@dataclass
class Image:
    universe: np.array
    expanded_universe: np.array = None


    def __post_init__(self):
        self.expand_universe()

    def expand_universe(self):
        expanded_universe = self.expand_rows(self.universe)
        expanded_universe = self.expand_columns(expanded_universe)
        self.expanded_universe = expanded_universe

    @staticmethod
    def expand_rows(universe):
        _, original_num_cols = universe.shape
        expanded_universe = np.empty((0, original_num_cols))
        for row in universe:
            expanded_universe = np.append(expanded_universe, row.reshape(1,-1), axis=0)
            if sum(row) == 0:
                expanded_universe = np.append(expanded_universe, row.reshape(1,-1), axis=0)

        return expanded_universe

    @staticmethod
    def expand_columns(universe):

        original_num_rows, _ = universe.shape
        expanded_universe = np.empty((original_num_rows, 0))
        for j in range(universe.shape[1]):
            col = universe[:, j].reshape(-1,1)
            expanded_universe = np.append(expanded_universe, col, axis=1)
            if sum(col) == 0:
                expanded_universe = np.append(expanded_universe, col, axis=1)

        return expanded_universe


def parse_input(raw_input):

    galaxy_coords = []
    for row, line in enumerate(raw_input.split("\n")):
        for col, char in enumerate(list(line)):
            if char == "#":
                galaxy_coords.append((row, col))
    nrows = row 
    ncols = col

    universe = np.zeros([nrows+1, ncols+1])
    for coord in galaxy_coords:
        universe[coord] = 1

    return Image(universe=universe)


def get_sum_of_distances(universe):

    galaxy_coords = np.argwhere(universe == 1)
    distances = cdist(galaxy_coords, galaxy_coords, 'cityblock')
    result = distances.sum().sum()/2
    return result


test_input_raw = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

test_image = parse_input(test_input_raw)
assert get_sum_of_distances(test_image.expanded_universe) == 374


with open("inputs/day11.txt") as f:
    raw_input = f.read()
    image = parse_input(raw_input)

result = get_sum_of_distances(image.expanded_universe)
print(f"Sum of distances: {result}")
