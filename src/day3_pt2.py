import re
import math


test_input_raw = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

test_flag = False

if test_flag is True:
    input = [x for x in test_input_raw.split('\n')]
else:
    with open('inputs/day3.txt') as f:
        input = [x for x in f.read().split('\n')]


def matches_to_coordinates(row_idx, matches):

    """
    Return the coordinates of the matches in the row, along with the match value.
    """

    coordinates = []
    for match in matches:
        start_col, end_col = match.span() 
        match_value = match.group()

        _coordinates = set()
        for col_idx in range(start_col, end_col):
            _coordinates.add((row_idx, col_idx))  
        coordinates.append((match_value, (_coordinates)))

    return coordinates


def find_adjacent_coordinates(coords):
    """
    Return a set of all coordinates adjacent to the given set of coordinates.
    Adjacency includes horizontal, vertical, and diagonal proximity.
    All generated coordinates must be positive.
    """
    adjacent_coords = set()
    for x, y in coords:
        # Consider all combinations of adding -1, 0, or 1 to both x and y
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                new_x, new_y = x + dx, y + dy
                # Check if new coordinates are positive and not the same as the original
                if new_x >= 0 and new_y >= 0 and (new_x, new_y) != (x, y):
                    adjacent_coords.add((new_x, new_y))

    return adjacent_coords


# which symbols are used in the input?
symbols = {char for row in input for char in row if not char.isdigit() and char != '.'}
symbol_regex = '[' + ''.join(re.escape(symbol) for symbol in symbols) + ']'


# convert the input to coordinates
number_locations = []
symbol_locations = []
for row_idx, row in enumerate(input):

    number_matches = [match for match in re.finditer(r'[0-9]+', row)]
    if number_matches:
        _number_locations = matches_to_coordinates(row_idx, number_matches)
        number_locations.extend(_number_locations)

    for match in re.finditer(symbol_regex, row):
         _symbol_locations = matches_to_coordinates(row_idx, [match])
         symbol_locations.append(_symbol_locations)


gear_ratios = []
for symbol_location in symbol_locations:
    for symbol, symbol_coords in symbol_location:
        symbol_adjacent_coords = find_adjacent_coordinates(symbol_coords)

        adjacent_numbers = [int(number) for number, number_coords in number_locations if symbol_adjacent_coords.intersection(number_coords)]
        if len(adjacent_numbers) == 2:
            gear_ratio = math.prod(adjacent_numbers)
            gear_ratios.append(gear_ratio)
            print(f"symbol: {symbol}")
            print(f"symbol location: {symbol_coords}")
            print(f"symbol adjacent coords: {symbol_adjacent_coords}")
            print(f"adjacent numbers: {adjacent_numbers}")
            print(f"gear ratio: {gear_ratio}")

result = sum(gear_ratios)
print(f"gear_ratios: {gear_ratios}")
print(f"result: {result}")

