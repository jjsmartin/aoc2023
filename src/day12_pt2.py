from dataclasses import dataclass
from typing import Tuple
from functools import cache


@dataclass
class Record:
    conditions: str
    expected_sequences: Tuple[int]

    def __repr__(self):
        return f"Record: \nconditions={self.conditions} \nexpected_sequences={self.expected_sequences})\n"


def parse_records(input_raw: str) -> Tuple[Record]:

    """Take the raw input and return a tuple of records."""

    records = []
    for line in input_raw.splitlines():
        conditions, expected_sequences = line.split(' ')

        expected_sequences = tuple(int(expected_sequence) for expected_sequence in expected_sequences.split(','))

        record = Record(conditions, expected_sequences)
        records.append(record)

    return records


@cache
def count_valid_arrangements(line, expected_hash_sequences, actual_hash_sequences=(), hash_count=0, idx=0) -> int:

    """
    How many valid arrangements are there for the given line?
    This will be either 1 or 0 if there are no question marks; potentially more otherwise.
    """

    # Base cases:
    if idx == len(line):

        # deal with any hash sequence that was in progress at the end of the line
        if hash_count > 0:
            actual_hash_sequences += (hash_count,)

        if expected_hash_sequences == actual_hash_sequences:
            result = 1
        else:
            result = 0
    
    elif len(actual_hash_sequences) > len(expected_hash_sequences):
        result = 0

    elif len(actual_hash_sequences) > 0 and actual_hash_sequences[-1] != expected_hash_sequences[len(actual_hash_sequences)-1]:
        result = 0

    # Recursive cases:
    elif line[idx] == '#':
        result = _process_hash(line, expected_hash_sequences, actual_hash_sequences, hash_count, idx)

    elif line[idx] == '.':
        result = _process_dot(line, expected_hash_sequences, actual_hash_sequences, hash_count, idx)

    elif line[idx] == '?':
        result_if_hash = _process_hash(line, expected_hash_sequences, actual_hash_sequences, hash_count, idx)
        result_if_dot = _process_dot(line, expected_hash_sequences, actual_hash_sequences, hash_count, idx)
        result = result_if_hash + result_if_dot

    else:
        raise ValueError(f"Invalid character: {line[idx]} at index {idx} in {line}")

    return result


def _process_hash(line, expected_hash_sequences, actual_hash_sequences, hash_count, idx):
    """If we see a hash, we count it and continue."""
    return count_valid_arrangements(line, expected_hash_sequences, actual_hash_sequences, hash_count+1, idx+1)


def _process_dot(line, expected_hash_sequences, actual_hash_sequences, hash_count, idx):
    """
    If we see a dot, and we were previously in a hash sequence, then that sequence has ended and we count it.
    Whether or not we were in a hash sequence, we continue with a hash count of 0.
    """
    if hash_count > 0:
        actual_hash_sequences += (hash_count,)

    return count_valid_arrangements(line, expected_hash_sequences, actual_hash_sequences, 0, idx+1)


def part1_count(input_raw):

    records = parse_records(input_raw)  

    result = 0
    for record in records:
        _result = count_valid_arrangements(record.conditions, record.expected_sequences )
        result += _result

    return result


def part2_count(input_raw, expansion_factor):

    records = parse_records(input_raw)  

    result = 0
    for record in records:
        # expand the record to the appropriate length
        line = '?'.join([record.conditions] * expansion_factor) 
        expected_hash_sequences = record.expected_sequences * expansion_factor
        _result = count_valid_arrangements(line, expected_hash_sequences)
        result += _result

    return result


test_input_raw = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

assert part1_count(test_input_raw) == 21
assert part2_count(test_input_raw, expansion_factor=5) == 525152


with open('inputs/day12.txt') as f:
    input_raw = f.read()

result_part_1 = part1_count(input_raw)
print(f"Part 1 Result: {result_part_1}")  # 7110

result_part_2 = part2_count(input_raw, expansion_factor=5)
print(f"Part 2 Result: {result_part_2}")  # 1566786613613

