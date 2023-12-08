import re
import math

from typing import Dict, List
from dataclasses import dataclass
from collections import namedtuple


test_input_raw = """Time:      7  15   30
Distance:  9  40  200"""


def parse_input(input_raw: str) -> Dict[str, Dict[str, int]]:

    times, distances = input_raw.split('\n')
    times = [int(x) for x in re.findall(r'\d+', times)]
    distances = [int(x) for x in re.findall(r'\d+', distances)]

    races = [ ]
    for time, distance in zip(times, distances):
        races.append(Race(time, distance))

    return Document(races)



Race = namedtuple('Race', ['time', 'distance'])


@dataclass
class Document:
    races: List[Race]


test_flag = False

if test_flag is True:
    document = parse_input(test_input_raw)

else:
    with open('inputs/day6.txt') as f:
        input_raw = f.read()
        document = parse_input(input_raw)


def lower_and_upper_bounds(race):

    """
    Upper and lower bounds for the time to match the record,
    obtained by solving the quadratic equation for the distance covered in the available time: (t-x)*x = d -> x^2 - tx + d = 0
    """

    a = (race.time - math.sqrt(race.time**2 - 4*race.distance)) / 2
    b = (race.time + math.sqrt(race.time**2 - 4*race.distance)) / 2

    upper_bound = max(a,b)
    lower_bound = min(a,b)

    # we want the integer above the lower bound, and the integer below the upper bound;
    #  this handles the case where a bound *is* an integer
    return math.floor(lower_bound+1), math.ceil(upper_bound - 1) 


result = 1
for race in document.races:
    print(race)
    lower_bound, upper_bound = lower_and_upper_bounds(race) 
    print(lower_bound, upper_bound)
    successes = (upper_bound - lower_bound) + 1
    print(f"There are {successes} possible ways to beat the distance record.")

    result *= successes

    print("--------------------")
    
print(result)




