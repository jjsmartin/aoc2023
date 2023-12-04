import re

test_input_raw = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

test_flag = False

if test_flag is True:
    input = [x for x in test_input_raw.split('\n')]
else:
    with open('inputs/day2.txt') as f:
        input = [x for x in f.read().split('\n')]


def parse_games(input):
    parsed_games = {}
    for game in input:
        parts = [part.strip() for part in re.split(';|:', game)]
        game_number = int(parts[0].split(' ')[1])

        draws = [re.split(',', part) for part in parts[1:]]
        parsed_draws = []
        for draw in draws:
            parsed_draw = {colour:int(count) for count,colour in [re.split(' ', x.strip()) for x in draw]}
            parsed_draws.append(parsed_draw)

        parsed_games[game_number] = parsed_draws

    return parsed_games



#bag = 12 red cubes, 13 green cubes, and 14 blue cubes
bag = {'red':12, 'green':13, 'blue':14}

parsed_games = parse_games(input)

result = 0
for game_number, draws in parsed_games.items():
    print(f'Game {game_number}:')
    print(f'  Bag: {bag}')
    print(f'  Draws: {draws}')

    impossible_draw = False
    for draw in draws:
        if impossible_draw is True:
            break
        for colour in bag.keys():

            number_in_bag = bag[colour]
            number_in_draw = draw.get(colour, 0)
            if number_in_draw > number_in_bag:
                print(f'    Invalid draw: {number_in_draw} {colour} cubes, only {number_in_bag} in bag')
                impossible_draw = True

    if impossible_draw is False:
        result += game_number

    print()

print(result)

