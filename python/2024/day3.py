# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import re

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_strings_from_lines(string):
    return list(string.splitlines())


def get_string_from_file(file_path=top_dir + "resources/year2024_day3_input.txt"):
    with open(file_path) as f:
        return get_strings_from_lines(f.read())


def get_mult_sum(strings):
    s = " ".join(strings)
    return sum(int(a) * int(b) for a, b in re.findall("mul\((\d+),(\d+)\)", s))


def get_enabled_mult_sum(strings):
    s = " ".join(strings)
    sum_ = 0
    do = True
    for instr, a, b in re.findall("(mul\((\d+),(\d+)\)|don't\(\)|do\(\))", s):
        if instr == "don't()":
            do = False
        elif instr == "do()":
            do = True
        elif do:
            sum_ += int(a) * int(b)
    return sum_


def run_tests():
    strings = get_strings_from_lines(
        """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""
    )
    assert get_mult_sum(strings) == 161
    strings = get_strings_from_lines(
        """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""
    )
    assert get_enabled_mult_sum(strings) == 48


def get_solutions():
    string = get_string_from_file()
    print(get_mult_sum(string) == 184576302)
    print(get_enabled_mult_sum(string) == 118173507)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
