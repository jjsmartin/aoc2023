import re
from dataclasses import dataclass
from typing import List, Set


test_input_raw = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


def parse_pile(raw: str) -> 'Pile':

    """Parse the raw input into a Pile object, containing Scratchcard objects."""

    scratchcards = []
    for line in raw.splitlines():
        new_scratchcard = parse_scratchcard(line)
        scratchcards.append(new_scratchcard)

    return Pile(scratchcards=scratchcards)

def parse_scratchcard(line: str) -> 'Scratchcard':

    """Parse one line of the raw input into a Scratchcard object."""

    card_name, numbers = line.split(': ')
    card_number = int(re.search(r'\d+', card_name).group())

    winning_numbers, revealed_numbers = numbers.split(' | ')

    winning_numbers = {int(num) for num in winning_numbers.split()}
    revealed_numbers = {int(num) for num in revealed_numbers.split()}

    return Scratchcard(card_number, winning_numbers, revealed_numbers)

@dataclass
class Scratchcard:
    id: int
    winning_numbers: Set[int]      
    revealed_numbers: Set[int]  
    matching_numbers: Set[int] = None
    value: int = None

    def __post_init__(self):
        """Calculate the value of the scratchcard."""
        self.matching_numbers = len(self.winning_numbers.intersection(self.revealed_numbers))
        if self.matching_numbers == 0:
            self.value = 0
        else:
            self.value = 2**(self.matching_numbers-1)


@dataclass
class Pile:
    scratchcards: List[Scratchcard]
    value: int = None

    def __post_init__(self):
        """Calculate the value of the pile."""
        self.value = sum([scratchcard.value for scratchcard in self.scratchcards])




test_flag = True

if test_flag is True:
    pile = parse_pile(test_input_raw)
else:
    with open('inputs/day4.txt') as f:
        input_raw = f.read()
        pile = parse_pile(input_raw)

print(f"The value of the pile is: {pile.value}")
