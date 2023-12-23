from collections import namedtuple

Node = namedtuple('Node', ['row', 'col', 'arrived_from'])

class EmptyTile():

    def __init__(self, row, col, energized):
        self.row = row 
        self.col = col 
        self.activated = False

    def __repr__(self):
        return f"{self.__class__.__name__} at ({self.row}, {self.col}), arrived from {self.arrived_from}. Activated: {self.activated}"

    def get_next_nodes(self, arrived_from):

        next_nodes = []
        if arrived_from == 'above':
            next_nodes.append(self.activate_down())
            
        elif arrived_from == 'below':
            next_nodes.append(self.activate_up())

        elif arrived_from == 'left':
            next_nodes.append(self.activate_right())

        elif arrived_from == 'right':
            next_nodes.append(self.activate_left())

        else:
            raise ValueError()

        return [node for node in next_nodes if node is not None]

    # go left and tell the next node we came from its right, and so on
    def activate_left(self):
        if self.col - 1 >= 0:
            return Node(self.row, self.col - 1, 'right')

    def activate_right(self):
        if self.col + 1 < GRID_WIDTH:
            return Node(self.row, self.col + 1, 'left')

    def activate_up(self):
        if self.row - 1 >= 0:
            return Node(self.row - 1, self.col, 'below')

    def activate_down(self):
        if self.row + 1 < GRID_HEIGHT:
            return Node(self.row + 1, self.col, 'above')



class VerticalSplitterTile(EmptyTile):
    def __init__(self, row, col, energized):
        super().__init__(row, col, energized)

    def get_next_nodes(self, arrived_from):

        next_nodes = []

        # splitting case
        if arrived_from in ['left', 'right']:
            next_nodes.append(self.activate_up())
            next_nodes.append(self.activate_down())

        # pointy end cases
        elif arrived_from == 'above':
            next_nodes.append(self.activate_down())

        elif arrived_from == 'below':
            next_nodes.append(self.activate_up())

        else:
            raise ValueError()

        return [node for node in next_nodes if node is not None]


class HorizontalSplitterTile(EmptyTile):
    def __init__(self, row, col, energized):
        super().__init__(row, col, energized)

    def get_next_nodes(self, arrived_from):

        next_nodes = []

        # splitting case
        if arrived_from in ['above', 'below']:
            next_nodes.append(self.activate_left())
            next_nodes.append(self.activate_right())

        # pointy end cases
        elif arrived_from == 'right':
            next_nodes.append(self.activate_left())

        elif arrived_from == 'left':
            next_nodes.append(self.activate_right())

        else:
            raise ValueError()

        return [node for node in next_nodes if node is not None]


class BackwardMirrorTile(EmptyTile):
    def __init__(self, row, col, energized):
        super().__init__(row, col, energized)

    def get_next_nodes(self, arrived_from):
        
        next_nodes = []
        if arrived_from == 'above':
            next_nodes.append(self.activate_right())
            
        elif arrived_from == 'below':
            next_nodes.append(self.activate_left())

        elif arrived_from == 'left':
            next_nodes.append(self.activate_down())

        elif arrived_from == 'right':
            next_nodes.append(self.activate_up())

        else:
            raise ValueError()

        return [node for node in next_nodes if node is not None]


class ForwardMirrorTile(EmptyTile):
    def __init__(self, row, col, energized):
        super().__init__(row, col, energized)

    def get_next_nodes(self, arrived_from):

        next_nodes = []
        if arrived_from == 'above':
            next_nodes.append(self.activate_left())
            
        elif arrived_from == 'below':
            next_nodes.append(self.activate_right())

        elif arrived_from == 'left':
            next_nodes.append(self.activate_up())

        elif arrived_from == 'right':
            next_nodes.append(self.activate_down())

        else:
            raise ValueError()

        return [node for node in next_nodes if node is not None]
        

def tile_factory(row, col, char):

    if char == ".":
        return EmptyTile(row, col, False)

    elif char == "|":
        return VerticalSplitterTile(row, col, False)

    elif char == "-":
        return HorizontalSplitterTile(row, col, False)

    elif char == "\\":
        return BackwardMirrorTile(row, col, False)

    elif char == "/":
        return ForwardMirrorTile(row, col, False)

    else:
        raise ValueError(f"Unknown tile type: {char} for tile at ({row}, {col})")


def display_activated_tiles(tiles):

    grid_width, grid_height = len(tiles[0]), len(tiles)

    tile_map = [['.' for _ in range(grid_width)] for _ in range(grid_height)]

    activated_tiles = [tile for row in tiles for tile in row if tile.activated]

    for tile in activated_tiles:
        tile_map[tile.row][tile.col] = '#'

    for row in tile_map:
        print(''.join(row))


def parse_input(input):

    tiles = []
    lines = input.split("\n")
    for row, line in enumerate(lines):
        row_values = []
        for col, char in enumerate(line):
            row_values.append(tile_factory(row, col, char))
        tiles.append(row_values)

    return tiles


def Part1(input):

    # I reckon it's OK to do this...
    global GRID_WIDTH, GRID_HEIGHT

    tiles = parse_input(input)
    GRID_WIDTH, GRID_HEIGHT = len(tiles[0]), len(tiles)

    # start top left, having arrived from the left
    starting_node = Node(0, 0, 'left')

    frontier = {starting_node}
    dealt_with = set()
    while frontier:

        current_node = frontier.pop()

        # we just use the tile to track its own activation and tell us the next tiles to activate, given the arrived_from direction
        current_tile = tiles[current_node.row][current_node.col]
        current_tile.activated = True
        next_nodes = current_tile.get_next_nodes(current_node.arrived_from) 

        for node in next_nodes:
            if node in dealt_with:
                continue
            else: 
                dealt_with.add(node)
                frontier.add(node)



    activated_tiles = [tile for row in tiles for tile in row if tile.activated]
    result = len(activated_tiles)

    return result

test_input = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""

assert Part1(test_input) == 46


with open('inputs/day16.txt') as f:
    input = f.read()

# 7798
result = Part1(input)
print(f"Part 1 result: {result}")