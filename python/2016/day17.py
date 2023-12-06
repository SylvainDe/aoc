# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import hashlib
import collections


resource_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../resources/"


def get_passcode_from_file(file_path=resource_dir + "year2016_day17_input.txt"):
    with open(file_path) as f:
        for l in f:
            return l.strip()


def directions(path):
    h = hashlib.md5(path.encode("utf-8")).hexdigest()
    return [direction for char, direction in zip(h, "UDLR") if char in "bcdef"]


dir_coord = {
    "U": (0, -1),
    "D": (0, 1),
    "L": (-1, 0),
    "R": (1, 0),
}


def point_in_dir(point, direction):
    x, y = point
    dx, dy = dir_coord[direction]
    return (x + dx, y + dy)


def point_is_valid(point):
    x, y = point
    return 0 <= x <= 3 and 0 <= y <= 3


def paths(passcode):
    start = (0, 0)
    end = (3, 3)
    paths = collections.deque([(passcode, start)])
    while paths:
        path, pos = paths.popleft()
        if pos == end:
            assert path.startswith(passcode)
            yield path[len(passcode) :]
        else:
            for d in directions(path):
                pos2 = point_in_dir(pos, d)
                if point_is_valid(pos2):
                    paths.append((path + d, pos2))


def shortest_path(passcode):
    for p in paths(passcode):
        return p


def longest_path(passcode):
    p = list(paths(passcode))
    return len(p[-1]) if p else 0


def run_tests():
    assert directions("hijkl") == ["U", "D", "L"]
    assert directions("hijklD") == ["U", "L", "R"]
    assert directions("hijklDR") == []
    assert directions("hijklDU") == ["R"]
    assert directions("hijklDUR") == []
    assert shortest_path("hijkl") is None
    assert shortest_path("ihgpwlah") == "DDRRRD"
    assert shortest_path("kglvqrro") == "DDUDRLRRUDRD"
    assert shortest_path("ulqzkmiv") == "DRURDRUDDLLDLUURRDULRLDUUDDDRR"
    assert longest_path("hijkl") == 0
    assert longest_path("ihgpwlah") == 370
    assert longest_path("kglvqrro") == 492
    assert longest_path("ulqzkmiv") == 830


def get_solutions():
    passcode = get_passcode_from_file()
    print(shortest_path(passcode) == "RDDRLDRURD")
    print(longest_path(passcode) == 448)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
