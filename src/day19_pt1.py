import numpy as np 
import re
import operator

from collections import namedtuple, defaultdict
from typing import List, Union

Part = namedtuple("Part", ["x", "m", "a", "s"])


class Node():
    def __init__(self, name, left=None, right=None):
        self.name = name
        self.left = left 
        self.right = right 


class ConditionalNode(Node):
    def __init__(self, name, left, right, variable, left_range, right_range):
        super().__init__(name, left, right)
        self.variable = variable
        self.left_range = left_range
        self.right_range = right_range

    def __repr__(self):
        return f"ConditionalNode: {self.name}. Left to {self.left} if {self.variable} in {self.left_range}, else right to {self.right}"
        
    def get_next_node_name(self, part: Part) -> str:

        if self.variable == 'x':
            if self.left_range[0] <= part.x <= self.left_range[1]:
                return self.left

        elif self.variable == 'm':
            if self.left_range[0] <= part.m <= self.left_range[1]:
                return self.left
                
        elif self.variable == 'a':
            if self.left_range[0] <= part.a <= self.left_range[1]:
                return self.left
                
        elif self.variable == 's':
            if self.left_range[0] <= part.s <= self.left_range[1]:
                return self.left
                
        return self.right


class ReferenceNode(Node):
    def __init__(self, name, left, right, workflow):
        super().__init__(name, left, right)
        self.workflow = workflow

    def __repr__(self):
        return f"Reference node: {self.name}"


class TerminalNode(Node):
        def __init__(self, name, left, right):
            super().__init__(name, left, right)
    
        def __repr__(self):
            return f"TerminalNode node: {self.name}"


def parse_input(input_str):

    unparsed_workflows, unparsed_parts = input_str.split("\n\n")

    workflows = parse_workflows(unparsed_workflows)
    parts = [parse_part(p) for p in unparsed_parts.split("\n")]

    return workflows, parts


def parse_part(s: str) -> List[Part]:
    pairs = s.strip("{}").split(",")

    parsed = {key_value.split("=")[0]: int(key_value.split("=")[1])
              for key_value in pairs}

    part = Part(**parsed)

    return part


def parse_workflows(unparsed_workflows):

    workflows = {}
    for w in unparsed_workflows.split("\n"):     
        workflow_name, workflow_rules = w.replace("}", "").split("{")
        workflows[workflow_name] = workflow_rules.split(",")

    return workflows


def determine_rule_type(rule: str) -> str:

    if ":" in rule:
        rule_type = 'condition'
    elif rule in ['A', 'R']:
        rule_type = 'terminal' 
    else:
        rule_type = 'reference'

    return rule_type


def parse_conditional(rule: str) -> Node:
    if "<" in rule:
        variable, rhs = rule.split("<")
        threshold_value, output = rhs.split(":")

        node = ConditionalNode(
            name=rule, 
            left=output, 
            right=None, 
            variable=variable, 
            left_range=(LOWEST_PART_VALUE, int(threshold_value)-1),
            right_range=(int(threshold_value), HIGHEST_PART_VALUE))

    elif ">" in rule:
        variable, rhs = rule.split(">")
        threshold_value, output = rhs.split(":")

        node = ConditionalNode(
            name=rule, 
            left=output, 
            right=None, 
            variable=variable, 
            left_range=(int(threshold_value) + 1, HIGHEST_PART_VALUE),
            right_range=(LOWEST_PART_VALUE, int(threshold_value)))

    return node


def parse_reference(rule: str) -> Node:
    node = ReferenceNode(name=rule, left=None, right=None, workflow=rule)
    return node


def parse_terminal(rule: str) -> Node:
    node = TerminalNode(name=rule, left=None, right=None)
    return node


LOWEST_PART_VALUE = 1
HIGHEST_PART_VALUE = 4000

test_input_raw = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""

with open("inputs/day19.txt") as f:
    input_raw = f.read()

workflows, parts = parse_input(input_raw)


nodes = {}
for workflow_name, rules in workflows.items():
    for rule in rules:
        rule_type = determine_rule_type(rule) 

        if rule_type == 'condition':
            node = parse_conditional(rule)
        elif rule_type == 'terminal':
            node = parse_terminal(rule)
        elif rule_type == 'reference':
            node = parse_reference(rule)
        else:
            raise ValueError(f"Unknown rule type {rule_type}")

        nodes[(workflow_name, node.name)] = node
    

for workflow_name, node_names in workflows.items():
    
    for i in range(len(node_names)-1):

        current_node_name = node_names[i]
        next_node_name = node_names[i+1]

        nodes[(workflow_name, current_node_name)].right = next_node_name


# PART 1
accepted_parts = []
accepted = 0
for part in parts:
    current_workflow_name = 'in'
    current_workflow = workflows[current_workflow_name]
    current_node_name = current_workflow[0]

    while True:
        if determine_rule_type(current_node_name) == 'terminal':
            if current_node_name == 'A':
                accepted += 1
                accepted_parts.append(part)
            break

        elif determine_rule_type(current_node_name) == 'reference':
            new_workflow_name = current_node_name
            new_workflow = workflows[new_workflow_name]
            current_node_name = new_workflow[0]
            current_workflow_name = new_workflow_name

        elif determine_rule_type(current_node_name) == 'condition':
            current_node = nodes[(current_workflow_name, current_node_name)]
            next_node_name = current_node.get_next_node_name(part)
            current_node_name = next_node_name
            
        else:
            raise ValueError(f"Unknown node type {type(current_node)}")

# 456651
result = sum([part.x + part.m + part.a + part.s for part in accepted_parts])
print(f"Part 1 result is {result}")