# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_rotation_from_line(string):
    letter, value = string[0], int(string[1:])
    return (1 if letter == "R" else -1), value


def get_rotations_from_lines(string):
    return [get_rotation_from_line(l) for l in string.splitlines()]


def get_rotations_from_file(file_path=top_dir + "resources/year2025_day1_input.txt"):
    with open(file_path) as f:
        return get_rotations_from_lines(f.read())


def get_positions(rotations):
    pos = 50
    for s, v in rotations:
        pos = (pos + s * v) % 100
        yield pos


def get_password(rotations):
    return sum(p == 0 for p in get_positions(rotations))


def get_password2(rotations):
    c = 0
    pos = 50
    for s, v in rotations:
        c -= s < 0 and pos == 0
        q, pos = divmod(pos + s * v, 100)
        c += abs(q)
        c += s < 0 and pos == 0
    return c


def run_tests():
    rotations = get_rotations_from_lines(
        """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""
    )
    assert get_password(rotations) == 3
    assert get_password2(rotations) == 6
    rotations = get_rotations_from_lines("""R1000""")
    assert get_password2(rotations) == 10


def get_solutions():
    rotations = get_rotations_from_file()
    print(get_password(rotations) == 1172)
    print(get_password2(rotations) == 6932)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
