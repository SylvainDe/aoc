# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_strings_from_lines(string):
    return string.splitlines()


def get_strings_from_file(file_path=top_dir + "resources/year2022_day25_input.txt"):
    with open(file_path) as f:
        return get_strings_from_lines(f.read())


from_snafu_digits = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2,
}

to_snafu_digits = {
    2: "2",
    1: "1",
    0: "0",
    -1: "-",
    -2: "=",
}


def snafu_to_dec(s):
    dec = 0
    for c in s:
        dec = 5 * dec + from_snafu_digits[c]
    return dec


def dec_to_snafu(n):
    s = []
    while n:
        # Add 2 then remove 2
        n, r = divmod(n + 2, 5)
        s.append(to_snafu_digits[r - 2])
    return "".join(reversed(s))


def solve(strings):
    return dec_to_snafu(sum(snafu_to_dec(s) for s in strings))


def run_tests():
    tests = [
        (1, "1"),
        (2, "2"),
        (3, "1="),
        (4, "1-"),
        (5, "10"),
        (6, "11"),
        (7, "12"),
        (8, "2="),
        (9, "2-"),
        (10, "20"),
        (15, "1=0"),
        (20, "1-0"),
        (2022, "1=11-2"),
        (12345, "1-0---0"),
        (314159265, "1121-1110-1=0"),
    ]
    for dec, snafu in tests:
        assert dec == snafu_to_dec(snafu)
        assert snafu == dec_to_snafu(dec)
    strings = get_strings_from_lines(
        """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"""
    )
    assert solve(strings) == "2=-1=0"


def get_solutions():
    strings = get_strings_from_file()
    print(solve(strings) == "2-20=01--0=0=0=2-120")


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
