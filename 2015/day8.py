# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_strings_from_file(file_path="day8_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]


def get_str_len_diff(s):
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


def run_tests():
    assert get_str_len_diff('""') == 2
    assert get_str_len_diff('"abc"') == 2
    assert get_str_len_diff('"aaa\\"aaa"') == 3
    assert get_str_len_diff('"\\x27"') == 5


def get_solutions():
    strings = get_strings_from_file()
    print(sum(get_str_len_diff(s) for s in strings))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
