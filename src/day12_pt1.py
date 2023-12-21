import re 

from collections import defaultdict
from dataclasses import dataclass
from typing import List


@dataclass
class Record:
    conditions: str
    sizes: List[int]

    def __repr__(self):
        return f"Record: \nconditions={self.conditions} \nsizes={self.sizes})\n"

    def unknown_locations(self):
        """indices of "?" locations in conditions"""
        return [i for i, condition in enumerate(self.conditions) if condition == "?"]



def parse_records(input_raw: str) -> List[Record]:
    records = []
    for line in input_raw.splitlines():
        conditions, sizes = line.split(' ')
        #conditions = list(conditions)
        sizes = [int(size) for size in sizes.split(',')]
        record = Record(conditions, sizes)
        records.append(record)

    return records

def generate_replacements(conditions, known_chars = ['.', '#'], wildcard_char = '?'):

    if wildcard_char not in conditions:
        return [conditions]

    else:
        results = []
        for char in known_chars:
            replaced = conditions.replace(wildcard_char, char, 1)
            results.extend(generate_replacements(replaced, known_chars, wildcard_char))
        
    return results

def count_consecutive_characters(conditions: str, target_char: str = '#') -> List[int]:

    # match any character, followed by 0 or more of the same character
    pattern = rf'{target_char}+'
    matches = re.findall(pattern, conditions)

    return [len(match) for match in matches]


def is_valid_replacements(replacement, sizes):
    counts = count_consecutive_characters(replacement)
    return counts == sizes


def count_arrangements(records):

    num_replacements = defaultdict(int)
    for i, record in enumerate(records):
        replacements = generate_replacements(record.conditions)
        for replacement in replacements:
            is_valid = (is_valid_replacements(replacement, record.sizes))
            if is_valid:
                num_replacements[i] += 1

    return sum(num_replacements.values())



test_input_raw = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

test_records = parse_records(test_input_raw)
assert count_arrangements(test_records) == 21

with open('inputs/day12.txt') as f:
    input_raw = f.read()
    records = parse_records(input_raw)

result = count_arrangements(records)
print(f"There are {result} valid arrangements")
