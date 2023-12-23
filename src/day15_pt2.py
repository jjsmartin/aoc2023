import re 
from collections import namedtuple, defaultdict
from typing import List

Step = namedtuple('Step', ['label', 'operation', 'focal_length', 'box_number'])
#Box = SortedList(key=lambda x: x[0])

# def box():
#     SortedList(key=lambda x: x[0])

def parse_input(input: str) -> List[Step]:

    input = input.replace('\n', '')
    steps_string = input.split(',')
    steps_parts = [re.split(r'(\W+)', s) for s in steps_string]

    steps = []
    for step_parts in steps_parts:
        label, operations, focal_length = step_parts
        if focal_length == '':
            focal_length = None
        else:
            focal_length = int(focal_length)

        box_number = HASH(label)

        steps.append(Step(label, operations, focal_length, box_number))

    return steps


def HASH(step):
    current_value = 0
    for character in step:
        current_value += ord(character)
        current_value *= 17
        current_value = current_value % 256

    return current_value


def focusing_power(box_number, box):

    focusing_power = 0
    for slot_number, focal_length in enumerate(box.values()):
        focusing_power += (slot_number+1) * focal_length

    focusing_power *= box_number + 1

    return focusing_power


def part2(input):

    steps = parse_input(input)
    boxes = defaultdict(dict)

    # run the initialization sequence 
    for step in steps:

        if step.operation == '=':

            # If there is already a lens in the box with the same label...
            if step.label in boxes.get(step.box_number, []):

                #...replace the old lens with the new lens 
                boxes[step.box_number][step.label] = step.focal_length

            else:
                # add the lens to the box immediately behind any lenses already
                boxes[step.box_number].update({step.label: step.focal_length})

        elif step.operation == '-':

            # remove the lens with the given label if it is present in the box.
            if step.label in boxes.get(step.box_number, []):
                    boxes[step.box_number].pop(step.label)

    # remove empty boxes
    boxes = {k: v for k, v in boxes.items() if v}

    fp = [focusing_power(box_number, box) for box_number, box in boxes.items()]
    result = sum(fp)

    return result

test_input = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""
assert part2(test_input) == 145

with open("inputs/day15.txt") as f:
    input = f.read()

# 229271
result = part2(input)
print(f"Part 2 Result: {result}")
