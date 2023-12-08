import re
import functools 

from dataclasses import dataclass
from typing import List, Set, Dict
from collections import namedtuple


test_input_raw = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

MappingRange = namedtuple('MappingRange', ['destination_start', 'source_start', 'length'])

def parse_almanac(raw):
    parts = raw.split('\n\n')
    seeds = parse_seeds(parts[0])
    raw_maps = parts[1:]
    maps = [parse_map(raw_map) for raw_map in raw_maps]

    return Almanac(seeds, maps)

def parse_seeds(raw):
    seeds = [int(n) for n in re.findall(r'\d+', raw)]
    return seeds

def parse_map(raw):
    parts = raw.split('\n')
    name = parts[0].split(' ')[0].strip()  # "seed-to-soil map" -> "seed-to-soil"
    mapping_ranges = []

    for line in parts[1:]:
        destination_start, source_start, length = [int(n) for n in line.split(' ')]
        mapping_ranges.append(MappingRange(destination_start, source_start, length))

    return Map(name, mapping_ranges)


@dataclass
class Map:
    name: str
    mapping: List[MappingRange]

    def lookup(self, n):
        for mapping_range in self.mapping:
            if n in range(mapping_range.source_start, mapping_range.source_start + mapping_range.length):
                return n - mapping_range.source_start + mapping_range.destination_start

        # return the original number if it's not in any of the ranges
        return n


@dataclass
class Almanac:
    seeds: List[int]
    maps: Dict[str, Dict[int, int]]

    def __post_init__(self):
        """Put the maps into a dictionary for easy lookup."""
        self.maps = {map.name: map for map in self.maps}

    def lookup(self, map_name, n):
        """Do the lookup in the specified map"""
        return self.maps[map_name].lookup(n)

    def get_seed_location(self, seed):
        # seed to soil to fertilizer to water to light to temperature to humidity to location
        soil = self.lookup('seed-to-soil', seed)
        fertilizer = self.lookup('soil-to-fertilizer', soil)
        water = self.lookup('fertilizer-to-water', fertilizer)
        light = self.lookup('water-to-light', water)
        temperature = self.lookup('light-to-temperature', light)
        humidity = self.lookup('temperature-to-humidity', temperature)  
        location = self.lookup('humidity-to-location', humidity)

        return location




test_flag = False

if test_flag is True:
    almanac = parse_almanac(test_input_raw)

    assert almanac.lookup('seed-to-soil', 79) == 81
    assert almanac.lookup('seed-to-soil', 14) == 14
    assert almanac.lookup('seed-to-soil', 55) == 57
    assert almanac.lookup('seed-to-soil', 13) == 13

else:
    with open('inputs/day5.txt') as f:
        input_raw = f.read()
        almanac = parse_almanac(input_raw)

seed_locations = [almanac.get_seed_location(seed) for seed in almanac.seeds]
result = min(seed_locations)

print(almanac)
print(seed_locations)
print(result)

