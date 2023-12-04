import re

with open('inputs/day1.txt') as f:
    input = [x for x in f.read().split('\n')]

test_input_raw = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

test_input = [x for x in test_input_raw.split('\n')]

digit_lookup = {word:digit+1 for digit,word in enumerate(['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'])}
for idx, digit in enumerate([1,2,3,4,5,6,7,8,9]):
    digit_lookup[str(idx+1)] = digit

pattern = '|'.join(re.escape(word) for word in digit_lookup.keys())

result = 0
#for line in test_input:
for line in input:
    first_match = re.search(pattern, line)
    last_match = re.search(pattern[::-1],line[::-1])

    calibration_value = [digit_lookup[first_match.group()] * 10 + digit_lookup[last_match.group()[::-1]]][0]
    result += calibration_value

print(result)