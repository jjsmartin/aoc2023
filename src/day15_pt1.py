def parse_input(input):

    # remove newlines
    input = input.replace('\n', '')
    
    steps = input.split(',')

    steps = [list(step) for step in steps]

    return steps


def HASH(step):
    current_value = 0
    for character in step:
        current_value += ord(character)
        current_value *= 17
        current_value = current_value % 256

    return current_value


def part1(input):
    sequence = parse_input(input)

    decoded = []
    for step in sequence:
        decoded.append(HASH(step))

    result = sum(decoded) 

    return result



test_input = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""
assert HASH(list("HASH")) == 52
assert part1(test_input) == 1320

with open("inputs/day15.txt") as f:
    input = f.read()

# 522547
result = part1(input)
print(f"Result: {result}")