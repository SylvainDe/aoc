# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import collections


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_instructions_from_file(file_path=top_dir + "resources/year2015_day1_input.txt"):
    with open(file_path) as f:
        for l in f:
            return l.strip()


def get_final_floor(instructions):
    c = collections.Counter(instructions)
    return c["("] - c[")"]


def get_position_to_basement(instructions, basement=-1):
    floor = 0
    values = {"(": 1, ")": -1}
    for i, ins in enumerate(instructions, start=1):
        floor += values[ins]
        if floor == basement:
            return i
    assert False


def run_tests():
    assert get_final_floor("(())") == 0
    assert get_final_floor("()()") == 0
    assert get_final_floor("(((") == 3
    assert get_final_floor("())") == -1
    assert get_position_to_basement(")") == 1
    assert get_position_to_basement("()())") == 5


def get_solutions():
    instructions = get_instructions_from_file()
    print(get_final_floor(instructions) == 232)
    print(get_position_to_basement(instructions) == 1783)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
