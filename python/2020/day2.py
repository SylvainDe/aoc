# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import re


LINE_RE = re.compile(r"(?P<mini>\d+)-(?P<maxi>\d+) (?P<letter>.): (?P<pwd>.*)")


def get_info_from_line(line):
    m = LINE_RE.fullmatch(line)
    if m is None:
        raise ValueError("Line did not match regular expression", line)
    mini, maxi, letter, pwd = m.groups()
    mini, maxi = int(mini), int(maxi)
    return (mini, maxi, letter, pwd)


def get_lines_from_file(file_path="day2_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]


def line_is_valid_pwd_part_1(line):
    mini, maxi, letter, pwd = get_info_from_line(line)
    count = pwd.count(letter)
    return mini <= count <= maxi


def line_is_valid_pwd_part_2(line):
    mini, maxi, letter, pwd = get_info_from_line(line)
    return sum(pwd[pos - 1] == letter for pos in (mini, maxi)) == 1


def run_tests():
    assert line_is_valid_pwd_part_1("1-3 a: abcde")
    assert not line_is_valid_pwd_part_1("1-3 b: cdefg")
    assert line_is_valid_pwd_part_1("2-9 c: ccccccccc")

    assert line_is_valid_pwd_part_2("1-3 a: abcde")
    assert not line_is_valid_pwd_part_2("1-3 b: cdefg")
    assert not line_is_valid_pwd_part_2("2-9 c: ccccccccc")


def get_solutions():
    lines = get_lines_from_file()
    print(sum(line_is_valid_pwd_part_1(l) for l in lines) == 542)
    print(sum(line_is_valid_pwd_part_2(l) for l in lines) == 360)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
