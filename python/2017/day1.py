# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_line_from_file(file_path="../../resources/year2017_day1_input.txt"):
    with open(file_path) as f:
        for l in f:
            return l.strip()


def get_solution(line, shift=None):
    if shift is None:
        shift = len(line) // 2
    return sum(int(c1) for c1, c2 in zip(line, line[shift:] + line[:shift]) if c1 == c2)


def run_tests():
    assert get_solution("", 1) == 0
    assert get_solution("1122", 1) == 3
    assert get_solution("1111", 1) == 4
    assert get_solution("1234", 1) == 0
    assert get_solution("91212129", 1) == 9
    assert get_solution("") == 0
    assert get_solution("1212") == 6
    assert get_solution("1221") == 0
    assert get_solution("123425") == 4
    assert get_solution("123123") == 12
    assert get_solution("12131415") == 4


def get_solutions():
    line = get_line_from_file()
    print(get_solution(line, 1) == 1069)
    print(get_solution(line) == 1268)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
