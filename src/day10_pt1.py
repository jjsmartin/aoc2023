import networkx as nx
import matplotlib.pyplot as plt

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Tile:
    type: str 
    i: int 
    j: int 
    connections = None

    def __repr__(self):
        return f"{self.type} at ({self.i}, {self.j})"

NORTH = (-1, 0)
SOUTH = (1, 0)
EAST = (0, 1)
WEST = (0, -1)

valid_moves = {

    ("|", "|"): [NORTH, SOUTH],
    ("|", "-"): [],
    ("|", "L"): [SOUTH],
    ("|", "J"): [SOUTH],
    ("|", "7"): [NORTH],
    ("|", "F"): [NORTH],
    ("|", "."): [],
    ("|", "S"): [NORTH, SOUTH],

    ("-", "|"): [],
    ("-", "-"): [EAST, WEST],
    ("-", "L"): [WEST],
    ("-", "J"): [EAST],
    ("-", "7"): [EAST],
    ("-", "F"): [WEST],
    ("-", "."): [],
    ("-", "S"): [EAST, WEST],

    ("L", "|"): [NORTH],
    ("L", "-"): [EAST],
    ("L", "L"): [],
    ("L", "J"): [EAST],
    ("L", "7"): [NORTH, EAST],
    ("L", "F"): [NORTH],
    ("L", "."): [],
    ("L", "S"): [NORTH, EAST],

    ("J", "|"): [NORTH],
    ("J", "-"): [WEST],
    ("J", "L"): [WEST],
    ("J", "J"): [],
    ("J", "7"): [NORTH],
    ("J", "F"): [NORTH, WEST],
    ("J", "."): [],
    ("J", "S"): [NORTH, WEST],

    ("7", "|"): [SOUTH],
    ("7", "-"): [WEST],
    ("7", "L"): [WEST, SOUTH],
    ("7", "J"): [SOUTH],
    ("7", "7"): [],
    ("7", "F"): [WEST],
    ("7", "."): [],
    ("7", "S"): [SOUTH, WEST],

    ("F", "|"): [SOUTH],
    ("F", "-"): [EAST],
    ("F", "L"): [SOUTH],
    ("F", "J"): [EAST, SOUTH],
    ("F", "7"): [EAST],
    ("F", "F"): [],
    ("F", "."): [],
    ("F", "S"): [EAST, SOUTH],
}


@dataclass
class Sketch:
    tiles: Dict
    start: Tile = None
    graph = None
    connections = None

    def __post_init__(self):
        self.start = [tile for tile in self.tiles.values() if tile.type == "S"][0]
        self.get_connections()
        self.create_graph()

    def get_connections(self):
        connections = []
        for tile in self.tiles.values():
            if tile.type == ".":
                continue

            connected_tiles = []
            for direction in [NORTH, SOUTH, EAST, WEST]:
                candidate_tile_coords = (tile.i + direction[0], tile.j + direction[1])  
                if candidate_tile_coords not in self.tiles:
                    continue
                candidate_tile = self.tiles[candidate_tile_coords]
                if self.is_valid_connection(tile, candidate_tile, direction):
                    #connected_tiles.append(candidate_tile) 
                    connections.append((tile, candidate_tile))

        # handle connections to the start tile
        adjacent_to_start = [tile 
                            for tile in self.tiles.values() 
                            if self.are_adjacent( (tile.i, tile.j), (self.start.i, self.start.j) )]

        # .....something is wrong here
        connected_to_start = []
        for tile in adjacent_to_start:
            for direction in [NORTH, SOUTH, EAST, WEST]:
                if tile.i + direction[0] == self.start.i and tile.j + direction[1] == self.start.j:
                    is_valid = self.is_valid_connection(tile, self.start, direction)
                    if is_valid:
                        connected_to_start.append(tile)
                        print(f"tile: {tile}, direction: {direction}, is_valid: {is_valid}")

        print(f"Start: {self.start}")
        print(f"adjacent_to_start: {adjacent_to_start}")
        print(f"connected_to_start: {connected_to_start}")

        self.connections = connections

    @staticmethod
    def is_valid_connection(from_tile, to_tile, direction):
        valid_directions = valid_moves.get((from_tile.type, to_tile.type), [])
        return direction in valid_directions

    @staticmethod
    def are_adjacent(coord1, coord2):
        x1, y1 = coord1
        x2, y2 = coord2
        return (x1 == x2 and abs(y1 - y2) == 1) or (y1 == y2 and abs(x1 - x2) == 1)

    def create_graph(self):

        G = nx.Graph()
        #print(f"sketch.connections: {self.connections}")
        for tile, connected_tile in self.connections:
            tile_coords = (tile.i, tile.j)
            connected_tile_coords = (connected_tile.i, connected_tile.j)
            G.add_edge(tile_coords, connected_tile_coords)

        cycles = nx.cycle_basis(G)

        nodes_in_cycles = set()
        for cycle in cycles:
            nodes_in_cycles.update(cycle)

        nodes_to_remove = [node for node in G if node not in nodes_in_cycles]
        for node in nodes_to_remove:
            G.remove_node(node)

        self.graph = G


    def get_furthest_distance(self):
        start = (self.start.i, self.start.j)
        path_lengths = nx.single_source_shortest_path_length(self.graph, start)
        furthest_distance = max(path_lengths.values())
        
        return furthest_distance



def parse_sketch(raw: str):  

    coords = {}
    for i, row in enumerate(raw.split('\n')):
        for j, tile_type in enumerate(row):
            coords[(i,j)] = (Tile(tile_type, i, j))

    sketch = Sketch(coords)

    return sketch





test_input_raw_1 = """.....
.S-7.
.|.|.
.L-J.
....."""
test_sketch_1 = parse_sketch(test_input_raw_1)  # 4
# nx.draw(test_sketch_1.graph, with_labels=True, node_color='lightblue', edge_color='gray')
# plt.show()


test_input_raw_2 = """..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""
test_sketch_2 = parse_sketch(test_input_raw_2) # 8
# nx.draw(test_sketch_2.graph, with_labels=True, node_color='lightblue', edge_color='gray')
# plt.show()

assert test_sketch_1.get_furthest_distance() == 4
assert test_sketch_2.get_furthest_distance() == 8



with open("inputs/day10.txt") as f:
    input_raw = f.read()
    sketch = parse_sketch(input_raw)

print(f"Result: {sketch.get_furthest_distance()}")

