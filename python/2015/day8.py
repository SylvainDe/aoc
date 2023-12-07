# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_strings_from_file(file_path=top_dir + "resources/year2015_day8_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]


def get_str_len_diff_decode(s):
    char_diff = {
        "\\": 1,
        '"': 1,
        "x": 3,
    }
    count = 2  # first and last quotes
    skip = False
    for c1, c2 in zip(s, s[1:]):
        if skip:
            skip = False
        elif c1 == "\\":
            count += char_diff[c2]
            skip = True
    return count


def get_str_len_diff_encode(s):
    char_diff = {
        '"': 1,
        "\\": 1,
    }
    count = 2  # first and last quotes
    for c in s:
        count += char_diff.get(c, 0)
    return count


def run_tests():
    tests = [
        ('""', 2, 4),
        ('"abc"', 2, 4),
        ('"aaa\\"aaa"', 3, 6),
        ('"\\x27"', 5, 5),
    ]
    for s, d1, d2 in tests:
        assert get_str_len_diff_decode(s) == d1
        assert get_str_len_diff_encode(s) == d2


def get_solutions():
    strings = get_strings_from_file()
    print(sum(get_str_len_diff_decode(s) for s in strings) == 1342)
    print(sum(get_str_len_diff_encode(s) for s in strings) == 2074)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
