# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_string_from_line(string):
    return string


def get_strings_from_lines(string):
    return [get_string_from_line(l) for l in string.splitlines()]


def get_strings_from_file(file_path="../../resources/year2023_day1_input.txt"):
    with open(file_path) as f:
        return get_strings_from_lines(f.read())


def get_calibration_value(s):
    digits = [c for c in s if c.isdigit()]
    return 10 * int(digits[0]) + int(digits[-1])


def get_calibration_sum(strings):
    return sum(get_calibration_value(s) for s in strings)


def get_calibration_value2(s):
    digits_words = {
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
    digits = []
    for i, c in enumerate(s):
        if c.isdigit():
            digits.append(int(c))
        else:
            s2 = s[i:]
            for w, val in digits_words.items():
                if s2.startswith(w):
                    digits.append(val)
    return 10 * digits[0] + digits[-1]


def get_calibration_sum2(strings):
    return sum(get_calibration_value2(s) for s in strings)


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
