# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import collections


def get_point(string):
    x, y = string.split(",")
    return int(x), int(y)


def get_vent(string):
    left, right = string.strip().split(" -> ")
    return get_point(left), get_point(right)


def get_vents_from_file(file_path="day5_input.txt"):
    with open(file_path) as f:
        return [get_vent(l) for l in f]


def get_lines_overlaps(lines, diagonals=False):
    paths = collections.Counter()
    for (x1, y1), (x2, y2) in lines:
        dx, dy = x2 - x1, y2 - y1
        absdx, absdy = abs(dx), abs(dy)
        steps = None
        if dx == 0:
            steps = absdy
        elif dy == 0:
            steps = absdx
        elif diagonals and absdx == absdy:
            steps = absdx
        if steps is not None:
            for s in range(steps + 1):
                x = x1 + s * dx / steps
                y = y1 + s * dy / steps
                paths[(x, y)] += 1
    return sum(val > 1 for val in paths.values())


def run_tests():
    vents = [
        "0,9 -> 5,9",
        "8,0 -> 0,8",
        "9,4 -> 3,4",
        "2,2 -> 2,1",
        "7,0 -> 7,4",
        "6,4 -> 2,0",
        "0,9 -> 2,9",
        "3,4 -> 1,4",
        "0,0 -> 8,8",
        "5,5 -> 8,2",
    ]
    vents = [get_vent(s) for s in vents]
    assert get_lines_overlaps(vents) == 5
    assert get_lines_overlaps(vents, True) == 12


def get_solutions():
    vents = get_vents_from_file()
    print(get_lines_overlaps(vents))
    print(get_lines_overlaps(vents, True))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
