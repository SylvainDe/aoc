# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_shape_from_lines(string):
    return {
        (i, j)
        for i, l in enumerate(string.splitlines()[1:])
        for j, v in enumerate(l)
        if v == "#"
    }

def get_region_from_line(string):
    sep = ": "
    beg, mid, end = string.partition(sep)
    assert mid == sep
    dims = tuple(int(i) for i in beg.split("x"))
    qtys = tuple(int(i) for i in end.split(" "))
    return dims, qtys


def get_input_from_lines(string):
    lst = string.split("\n\n")
    shapes = tuple(get_shape_from_lines(s) for s in lst[:-1])
    regions = tuple(get_region_from_line(l) for l in lst[-1].splitlines())
    return shapes, regions


def get_input_from_file(file_path=top_dir + "resources/year2025_day12_input.txt"):
    with open(file_path) as f:
        return get_input_from_lines(f.read())


def run_tests():
    input_ = get_input_from_lines(
        """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2"""
    )
    print(input_)


def get_solutions():
    input_ = get_input_from_file()


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
