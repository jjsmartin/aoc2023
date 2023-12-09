from dataclasses import dataclass
from typing import List



@dataclass
class Sequence:
    values: List[int]

    def __repr__(self):
        return f"{self.values}"

    def get_differences(self):
        differences = [self.values[i] - self.values[i-1] for i in range(1, len(self.values))]
        return Sequence(differences)

    def get_next_sequence(self):
        if all(v == 0 for v in self.values):
            return None
        else:
            next_seq = self.get_differences()
            return next_seq


@dataclass
class History(Sequence):
    next_term: int = None

    def __post_init__(self):
        """Each new term is the sum of the previous elements in its own sequence and the last element in the previous sequence."""
        expanded = self.expand() 
        self.next_term = sum([seq.values[-1] for seq in expanded])

    def expand(self):
        seq = Sequence(self.values)
        seqs = []
        while True:
            if seq is None:
                break
            else:
                seqs.append(seq)
                seq = seq.get_next_sequence()
            
        return seqs


@dataclass 
class Report:
    histories: List[History]




def parse_report(raw):
    histories = []
    lines = raw.split('\n')
    for line in lines:
        values = [int(n) for n in line.split(' ')]
        histories.append(History(values))

    return Report(histories)




test_input_raw = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

test_report = parse_report(test_input_raw)
assert sum([hist.next_term for hist in test_report.histories]) == 114

with open('inputs/day9.txt') as f:
    input_raw = f.read()
    report = parse_report(input_raw)

result = sum([hist.next_term for hist in report.histories])  # 1904165718
print(f"Result: {result}")

