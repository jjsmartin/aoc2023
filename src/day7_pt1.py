from dataclasses import dataclass
from collections import namedtuple, Counter
from typing import List

Card = namedtuple('Card', ['label', 'rank'])

@dataclass 
class Hand:
    cards: List[Card] 
    bid: int
    type: str = None 
    type_rank: int = None  

    type_ranks = {
        'five_of_a_kind': 6,
        'four_of_a_kind': 5,
        'full_house': 4,
        'three_of_a_kind': 3,
        'two_pair': 2,
        'one_pair': 1,
        'high_card': 0
    }

    def __repr__(self):
        return f"{''.join(card.label for card in self.cards)}, {self.type}, bid: {self.bid}, type_rank: {self.type_rank}"

    def __post_init__(self):

        counts = Counter(self.cards).most_common()

        if counts[0][1] == 5:
            type = 'five_of_a_kind'

        elif counts[0][1] == 4: 
            type = 'four_of_a_kind'

        elif counts[0][1] == 3 and counts[1][1] == 2:
            type = 'full_house'

        elif counts[0][1] == 3:
            type = 'three_of_a_kind'

        elif counts[0][1] == 2 and counts [1][1] == 2: 
            type = 'two_pair'

        elif counts[0][1] == 2: 
            type = 'one_pair'

        else:
            type = 'high_card'

        self.type = type
        self.type_rank = self.type_ranks[type]



    def __gt__(self, other: 'Hand'):

        """Does this hand beat another one?"""

        if self.type_rank > other.type_rank:
            #print(f"first card wins: {self.type} beats {other.type}")
            return True 
        
        elif self.type_rank < other.type_rank:
            #print(f"second card wins: {self.type} loses to {other.type}")
            return False
        
        else:
            return self.hand_beats_by_high_card(other)


    def hand_beats_by_high_card(self, other: 'Hand'):

        """Given another hand of the same type, does this hand win?"""

        for self_card, other_card in zip(self.cards, other.cards):

            # lower rank is better here
            if self_card.rank < other_card.rank:
                #print(f"first card wins, by high card {self_card} beats {other_card}")
                return True
            
            elif other_card.rank < self_card.rank:
                #print(f"second card wins, by high card {self_card} loses to {other_card}")
                return False 
            
            else:
                continue
            
        # not possible to draw?
        return None 

def parse_hands(raw):
    lines = raw.split('\n')

    hands = {}
    for line in lines:
        card_labels, bid = line.split(' ')
        cards = [Card(label, card_ranks[label]) for label in card_labels]
        hands[card_labels] = Hand(cards, int(bid))
    
    return hands



test_flag = False

test_input_raw = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

card_types = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
card_ranks = {str(label):card_rank for card_rank, label in enumerate(card_types)}

if test_flag is False:
    with open("inputs/day7.txt") as f:
        input_raw = f.read()
        hands = parse_hands(input_raw)
else:
    hands = parse_hands(test_input_raw)



ordering = sorted(list(hands.values()))

winnings = sum([(1+idx) * hand.bid for idx, hand in enumerate(ordering)])
print(winnings)



