# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"

HEIGHT = 7

def measure_height(lst, idx, c):
    is_lock = c == "#"
    assert len(lst) == HEIGHT
    for i, l in enumerate(lst):
        if l[idx] != c:
            return i - 1 if is_lock else HEIGHT - i - 1
    assert None


def get_key_from_line(string):
    c = string[0]
    is_lock = c == "#"
    lst = string.splitlines()
    heights = [measure_height(lst, i, c) for i, _ in enumerate(lst[0])]
    return is_lock, heights


def get_keys_from_lines(string):
    return [get_key_from_line(s) for s in string.split("\n\n")]


def get_keys_from_file(file_path=top_dir + "resources/year2024_day25_input.txt"):
    with open(file_path) as f:
        return get_keys_from_lines(f.read())


def is_fit(key, lock):
    return all(a + b + 2 <= HEIGHT for a, b in zip(key, lock))

def get_nb_fits(keys):
    k, l = [], []
    for is_lock, heights in keys:
        (l if is_lock else k).append(heights)
    return sum(is_fit(key, lock) for key in k for lock in l)


def run_tests():
    keys = get_keys_from_lines(
        """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""
    )
    assert get_nb_fits(keys) == 3


def get_solutions():
    keys = get_keys_from_file()
    print(get_nb_fits(keys) == 3196)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
