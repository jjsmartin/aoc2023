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
    num_jokers = int = None 

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
        return f"{''.join(card.label for card in self.cards)}, {self.type}, bid: {self.bid}, type_rank: {self.type_rank}, Jokers: {self.num_jokers}"

    def __post_init__(self):
 
        self.num_jokers = len([card for card in self.cards if card.label == 'J'])

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

        #original_type = type

        # upgrade the hand according to the number of Jokers    
        if self.num_jokers > 0:

            # if we have 4 Jokers, we match the 5th card
            # if we have 4 of something else and the remaining card is a Joker, we match the 4
            if type == 'four_of_a_kind':
                type = 'five_of_a_kind'

            # in a 3/2 split, there must be either 2 or 3 Jokers; either way we can make them match the other group
            elif type == 'full_house':       
                if 2 <= self.num_jokers <= 3:
                    type = 'five_of_a_kind'

            # Since this case is not a full house, the other 2 cards must not match.
            # So either it's 3 Jokers, which we make match one of the other 2 cards, getting 4 of a kind
            #  or it's 1 Joker, which we make match one of the three of a kind, again getting 4 of a kind
            # We could also construct a full house from this situation, but four of a kind is always better
            elif type == 'three_of_a_kind':
                type = 'four_of_a_kind'

            # If one of the pairs is Jokers, we can get four of a kind by matching the other pair
            # if there's two pairs plus one Joker, we can make a full house
            elif type == 'two_pair':
                if self.num_jokers == 2:
                    type = 'four_of_a_kind'
                elif self.num_jokers == 1:
                    type = 'full_house'
            
            # If the pair was 2 Jokers, they would be the pair. In that case, the best we can do is make them match one of the other cards
            # otherwise, we must have just one Joker and we add it to the pair.
            elif type == 'one_pair':
                type = 'three_of_a_kind'          

            # if there was more than 1 Joker, we'd already have a pair or better
            elif type == 'high_card':
                type = 'one_pair'    
            
        self.type = type
        self.type_rank = self.type_ranks[type]

        # if type != original_type:
        #     print(f"Converting {original_type} -> {type} for {self}")
        #     print()


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

card_types = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
card_ranks = {str(label):card_rank for card_rank, label in enumerate(card_types)}

if test_flag is False:
    with open("inputs/day7.txt") as f:
        input_raw = f.read()
        hands = parse_hands(input_raw)
else:
    input_raw = test_input_raw
    hands = parse_hands(test_input_raw)

ordering = sorted(list(hands.values()))

winnings = sum([(1+idx) * hand.bid for idx, hand in enumerate(ordering)])
print(winnings)

