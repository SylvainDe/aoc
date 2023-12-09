# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_sequence_from_line(string):
    return [int(s) for s in string.split()]


def get_sequences_from_lines(string):
    return [get_sequence_from_line(l) for l in string.splitlines()]


def get_sequences_from_file(file_path=top_dir + "resources/year2023_day9_input.txt"):
    with open(file_path) as f:
        return get_sequences_from_lines(f.read())

def get_interpolated_value(sequence):
    if not any(sequence):
        return 0
    return sequence[-1] + get_interpolated_value([b - a for a, b in zip(sequence, sequence[1:])])


def get_interpolated_sum(sequences, forward):
    return sum(get_interpolated_value(seq if forward else list(reversed(seq)))
               for seq in sequences)

def run_tests():
    sequences = get_sequences_from_lines(
        """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""
    )
    assert get_interpolated_sum(sequences, True) == 114
    assert get_interpolated_sum(sequences, False) == 2


def get_solutions():
    sequences = get_sequences_from_file()
    print(get_interpolated_sum(sequences, True) == 1980437560)
    print(get_interpolated_sum(sequences, False) == 977)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
