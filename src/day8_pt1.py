import re

from typing import Dict, List
from dataclasses import dataclass
from collections import namedtuple



Node = namedtuple('Node', ['label', 'left', 'right'])

@dataclass
class Map:
    instructions: List[str]
    nodes: Dict[str, Node]

    def steps_to_zzz(self):

        node = self.nodes['AAA']
        i = 0
        while node.label != 'ZZZ':
            instruction = self.instructions[i%len(self.instructions)]
            next_node = node.left if instruction == 'L' else node.right
            print(f"At node {node}; instruction {instruction} so we go to {next_node}")
            node = self.nodes[next_node]

            if node != 'ZZZ':
                i += 1
        
        return i


test_input_raw_1 = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

test_input_raw_2 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""


def parse_map(raw):
    lines = raw.split('\n')
    instructions = list(lines[0])

    nodes = {}
    for line in lines[2:]:
        label, values = line.split(' = ')
        left, right = [v for v in values.replace('(', '').replace(')', '').split(', ')]
        nodes[label] = Node(label, left, right)

    return Map(instructions, nodes)



with open('inputs/day8.txt') as f:
    input_raw = f.read()

test_map_1 = parse_map(test_input_raw_1)
assert test_map_1.steps_to_zzz() == 2

test_map_2 = parse_map(test_input_raw_2)
assert test_map_2.steps_to_zzz() == 6

real_map = parse_map(input_raw)
part_1_result = real_map.steps_to_zzz()
print(f"Part 1: {part_1_result} steps to ZZZ")
