import re
import numpy as np

from typing import Dict, List, Set
from dataclasses import dataclass
from collections import namedtuple, defaultdict



Node = namedtuple('Node', ['label', 'left', 'right'])

@dataclass
class Map:
    instructions: List[str]
    nodes: Dict[str, Node]
    start_node_labels: Set[str] = None 
    end_node_labels: Set[str] = None

    def __post_init__(self):
        self.start_node_labels = {node.label for node in self.nodes.values() if node.label[-1] == 'A'}
        self.end_node_labels = {node.label for node in self.nodes.values() if node.label[-1] == 'Z'}

    def steps_to_end(self, start_node_label, end_node_label, max_steps=100_000):

        next_node_label = start_node_label
        i = 0
        finished = False
        reached_end_at = None
        already_seen = set()
        while not finished:
            current_node_label = next_node_label
            if current_node_label == end_node_label:
                reached_end_at = i
            instruction_number = i%len(self.instructions)
            instruction = self.instructions[instruction_number]
            next_node_label = self.nodes[current_node_label].left if instruction == 'L' else self.nodes[current_node_label].right
            #print(f"At node {current_node_label}; instruction {instruction} so we go to {next_node_label}")

            finished = (current_node_label == end_node_label) or ((instruction_number, current_node_label) in already_seen) or i > max_steps
            if not finished:
                i += 1
                already_seen.add((instruction_number, current_node_label))
        
        if i > max_steps:
            return None
        elif current_node_label == end_node_label:
            return reached_end_at



test_input_raw = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""


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

# Part 1
# test_map_1 = parse_map(test_input_raw_1)
# assert test_map_1.steps_to_end('AAA', 'ZZZ') == 2

# test_map_2 = parse_map(test_input_raw_2)
# assert test_map_2.steps_to_end('AAA', 'ZZZ') == 6

# real_map = parse_map(input_raw)
# part_1_result = real_map.steps_to_end('AAA', 'ZZZ') 
# #print(f"Part 1: {part_1_result} steps to ZZZ")
# assert part_1_result == 12169

# Part 2
part_2_map = parse_map(input_raw)

paths = {}
for start in part_2_map.start_node_labels:
    for end in part_2_map.end_node_labels:
        num_steps = part_2_map.steps_to_end(start, end, max_steps=1_000_000)
        paths[(start, end)] = num_steps

print(f"Start nodes: {part_2_map.start_node_labels}")
print(f"End nodes: {part_2_map.end_node_labels}")


for k,v in paths.items():
    if v is None:
        continue
    print(k, v)
    print()

# TODO should probably make sure that each start only connects to one end, but it turns out that way
result = np.lcm.reduce([v for v in paths.values() if v is not None])
print(result)
