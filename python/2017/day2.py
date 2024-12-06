# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import itertools


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_numbers_from_line(s):
    return [int(v) for v in s.split()]


def get_spreadsheet_from_file(file_path=top_dir + "resources/year2017_day2_input.txt"):
    with open(file_path) as f:
        return [get_numbers_from_line(l.strip()) for l in f]


def get_checksum(spreadsheet):
    return sum(max(l) - min(l) for l in spreadsheet)


def find_div(numbers):
    divs = [divmod(a, b) for a, b in itertools.permutations(numbers, 2)]
    cand = [q for q, r in divs if r == 0]
    assert len(cand) == 1
    return cand[0]


def get_div_sum(spreadsheet):
    return sum(find_div(l) for l in spreadsheet)


def run_tests():
    spreadsheet = [
        "5 1 9 5",
        "7 5 3",
        "2 4 6 8",
    ]
    spreadsheet = [get_numbers_from_line(l) for l in spreadsheet]
    assert get_checksum(spreadsheet) == 18
    spreadsheet = [
        "5 9 2 8",
        "9 4 7 3",
        "3 8 6 5",
    ]
    spreadsheet = [get_numbers_from_line(l) for l in spreadsheet]
    assert get_div_sum(spreadsheet) == 9


def get_solutions():
    spreadsheet = get_spreadsheet_from_file()
    print(get_checksum(spreadsheet) == 34581)
    print(get_div_sum(spreadsheet) == 214)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
