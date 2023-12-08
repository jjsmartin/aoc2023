import re
import functools 

from dataclasses import dataclass
from typing import List, Set, Dict
from collections import namedtuple, defaultdict


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
SeedRange = namedtuple('SeedRange', ['start', 'length'])

def parse_almanac(raw):
    parts = raw.split('\n\n')
    seed_ranges = parse_seed_ranges(parts[0])
    raw_maps = parts[1:]
    maps = [parse_map(raw_map) for raw_map in raw_maps]
    reverse_maps = [parse_reverse_map(raw_map) for raw_map in raw_maps]
    maps.extend(reverse_maps)

    return Almanac(seed_ranges, maps)

def parse_seed_ranges(raw) -> List[SeedRange]:
    numbers = [int(x) for x in raw.split(':')[1].strip().split(' ')]

    seed_ranges = [SeedRange(numbers[i], numbers[i+1]) for i in range(0, len(numbers), 2)]

    return seed_ranges

def parse_map(raw):
    parts = raw.split('\n')
    name = parts[0].split(' ')[0].strip()  # "seed-to-soil map" -> "seed-to-soil"
    mapping_ranges = []

    for line in parts[1:]:
        destination_start, source_start, length = [int(n) for n in line.split(' ')]
        mapping_ranges.append(MappingRange(destination_start, source_start, length))

    return Map(name, mapping_ranges)


def parse_reverse_map(raw):
    parts = raw.split('\n')
    name = parts[0].split(' ')[0].strip()  # "seed-to-soil map" -> "seed-to-soil"
    name = '-'.join(name.split('-')[::-1]) # "seed-to-soil" ->  "soil-to-seed"
    mapping_ranges = []

    for line in parts[1:]:
        source_start, destination_start, length = [int(n) for n in line.split(' ')]  # reverse the source and destination
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

    # def lookup_no_default(self, n):
    #     for mapping_range in self.mapping:
    #         if n in range(mapping_range.des_start, mapping_range.source_start + mapping_range.length):
    #             return n - mapping_range.source_start + mapping_range.destination_start
    #     return None


@dataclass
class Almanac:
    seed_ranges: List[SeedRange]
    maps: Dict[str, Dict[int, int]]

    def __post_init__(self):
        self.maps = {map.name: map for map in self.maps}

    def lookup(self, map_name, n):
        """Do the lookup in the specified map."""
        return self.maps[map_name].lookup(n)

    def get_seed_location(self, seed):
        """Map a seed to a location."""
        n = seed
        for mapping in ['seed-to-soil', 'soil-to-fertilizer', 'fertilizer-to-water', 'water-to-light', 'light-to-temperature', 'temperature-to-humidity', 'humidity-to-location']:
            n = self.lookup_no_default(mapping, n)
            if n is None:
                return None
        return location

    def get_location_seed(self, location):
        """Map a location back to a seed."""

        n = location
        for mapping in ['location-to-humidity', 'humidity-to-temperature', 'temperature-to-light', 'light-to-water', 'water-to-fertilizer', 'fertilizer-to-soil', 'soil-to-seed']:
            n = self.lookup(mapping, n)
            if n is None:
                return None
            if n in already_checked[mapping]:
                return None

        return n


already_checked = {
    'location-to-humidity': set(),
    'humidity-to-temperature': set(),
     'temperature-to-light': set(), 
     'light-to-water': set(), 
     'water-to-fertilizer': set(), 
     'fertilizer-to-soil': set(), 
     'soil-to-seed': set()
}


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


def location_has_seed(location):
    """does this location correspond to any of the initial seed numbers?"""
    seed = almanac.get_location_seed(location)

    for seed_range in almanac.seed_ranges:
        if seed in range(seed_range.start, seed_range.start + seed_range.length):
            return True
    else:
        return False


# check if a location corresponds to any of the initial seed numbers
best_seed = None
best_location = None
#location = 59370572  #best seed: 1623310249, best location: 59370572 
upper_limit = 59370572  #part 1 answer 
for location in range(0,upper_limit+1):

    if best_location is not None:
        break
    if best_seed is None:
        #print(f"checking location: {location}")
        seed = almanac.get_location_seed(location)
        print(f"location: {location}, seed: {seed}")
        print()
        if location_has_seed(location):
            best_seed = seed 
            best_location = location    
        else:
            continue

    location == 1

print(f"best seed: {best_seed}, best location: {best_location}")

