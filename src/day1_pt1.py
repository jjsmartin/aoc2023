with open('inputs/day1.txt') as f:
    input = [x for x in f.read().split('\n')]

test_input_raw = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

test_input = [x for x in test_input_raw.split('\n')]

def get_digits(line):
    digits = [x for x in line if x.isdigit()]
    return digits

# result = 0
# for line in test_input:
#     digits = get_digits(line) 
#     calibration_value = digits[0] + digits[-1]
#     result += int(calibration_value)

result = 0
for line in input:
    digits = get_digits(line) 
    calibration_value = digits[0] + digits[-1]
    result += int(calibration_value)


print(result)