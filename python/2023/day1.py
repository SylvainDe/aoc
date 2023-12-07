# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import string


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"

def get_string_from_line(string):
    return string


def get_strings_from_lines(string):
    return [get_string_from_line(l) for l in string.splitlines()]


def get_strings_from_file(file_path=top_dir + "resources/year2023_day1_input.txt"):
    with open(file_path) as f:
        return get_strings_from_lines(f.read())


map_digits = { d: int(d) for d in string.digits }

map_words = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

def find_values(s, mapping):
    for i in range(len(s)):
        s2 = s[i:]
        for k, v in mapping.items():
            if s2.startswith(k):
                yield v

def get_calibration_value(s, mapping):
    digits_found = list(find_values(s, mapping))
    return 10 * digits_found[0] + digits_found[-1]


def get_calibration_sum(strings):
    return sum(get_calibration_value(s, map_digits) for s in strings)


def get_calibration_sum2(strings):
    mapping = {**map_digits, **map_words}
    return sum(get_calibration_value(s, mapping) for s in strings)


def run_tests():
    strings = get_strings_from_lines(
        """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""
    )
    assert get_calibration_sum(strings) == 142
    strings = get_strings_from_lines(
        """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""
    )
    assert get_calibration_sum2(strings) == 281


def get_solutions():
    strings = get_strings_from_file()
    print(get_calibration_sum(strings) == 54634)
    print(get_calibration_sum2(strings) == 53855)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
