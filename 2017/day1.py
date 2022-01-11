# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_line_from_file(file_path="day1_input.txt"):
    with open(file_path) as f:
        for l in f:
            return l.strip()


def get_solution(line):
    if not line:
        return 0
    return sum(int(c1) for c1, c2 in zip(line, line[1:] + line[0]) if c1 == c2)


def run_tests():
    assert get_solution("") == 0
    assert get_solution("1122") == 3
    assert get_solution("1111") == 4
    assert get_solution("1234") == 0
    assert get_solution("91212129") == 9


def get_solutions():
    line = get_line_from_file()
    print(get_solution(line))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
