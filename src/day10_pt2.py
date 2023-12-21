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
    loop = None

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
                        #print(f"tile: {tile}, direction: {direction}, is_valid: {is_valid}")

        # print(f"Start: {self.start}")
        # print(f"adjacent_to_start: {adjacent_to_start}")
        # print(f"connected_to_start: {connected_to_start}")

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
        self.loop = cycles[0]

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




test_input_raw_1 = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""
test_sketch_1 = parse_sketch(test_input_raw_1)  
# nx.draw(test_sketch_1.graph, with_labels=True, node_color='lightblue', edge_color='gray')
# plt.show()


test_input_raw_2 = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""
test_sketch_2 = parse_sketch(test_input_raw_2) 
# nx.draw(test_sketch_2.graph, with_labels=True, node_color='lightblue', edge_color='gray')
# plt.show()

test_input_raw_3 = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJIF7FJ-
L---JF-JLJIIIIFJLJJ7
|F|F-JF---7IIIL7L|7|
|FFJF7L7F-JF7IIL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""
test_sketch_3 = parse_sketch(test_input_raw_3) 
# nx.draw(test_sketch_2.graph, with_labels=True, 


with open("inputs/day10.txt") as f:
    input_raw = f.read()
    sketch = parse_sketch(input_raw)


def count_cells_inside_loop(sketch):
    nrows = max([tile.i for tile in sketch.tiles.values()]) 
    ncols = max([tile.j for tile in sketch.tiles.values()]) 

    cell_count = 0
    for row in range(0, nrows+1):
        row_count = 0
        inside = False
        record = []
        for col in range(0, ncols+1):

            current_tile = sketch.tiles[(row,col)]

            if (current_tile.i, current_tile.j) in sketch.loop and current_tile.type in ["S", "|", "F", "7"]:
                inside = not inside
            
            elif inside and (current_tile.i, current_tile.j) not in sketch.loop :
                row_count += 1

            record.append(inside)
            
        cell_count += row_count

    return cell_count

assert count_cells_inside_loop(test_sketch_1) == 4
assert count_cells_inside_loop(test_sketch_2) == 8
assert count_cells_inside_loop(test_sketch_3) == 10


print(f"cell_count: { count_cells_inside_loop(sketch)}")

