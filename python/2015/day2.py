# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_dimensions_from_string(s):
    dims = [int(v) for v in s.split("x")]
    assert len(dims) == 3
    return dims


def get_dimensions_from_file(file_path="../../resources/year2015_day2_input.txt"):
    with open(file_path) as f:
        return [get_dimensions_from_string(l.strip()) for l in f]


def get_surface(dimensions):
    l, w, h = dimensions
    sides = [l * w, l * h, w * h]
    return 2 * sum(sides) + min(sides)


def get_length(dimensions):
    l, w, h = dimensions
    halfperi = [l + w, l + h, w + h]
    volume = l * w * h
    return 2 * min(halfperi) + volume


def run_tests():
    assert get_surface((2, 3, 4)) == 58
    assert get_surface((1, 1, 10)) == 43
    assert get_length((2, 3, 4)) == 34
    assert get_length((1, 1, 10)) == 14


def get_solutions():
    dimensions = get_dimensions_from_file()
    print(sum(get_surface(dim) for dim in dimensions) == 1586300)
    print(sum(get_length(dim) for dim in dimensions) == 3737498)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
