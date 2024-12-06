# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
from collections import Counter

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_numbers_from_line(string):
    return [int(s) for s in string.split()]


def get_numbers_from_lines(string):
    return [get_numbers_from_line(l) for l in string.splitlines()]


def get_numbers_from_file(file_path=top_dir + "resources/year2024_day1_input.txt"):
    with open(file_path) as f:
        return get_numbers_from_lines(f.read())


def transpose(numbers):
    return map(lambda *x: list(x), *numbers)


def get_total_distance(numbers):
    list1, list2 = transpose(numbers)
    return sum(abs(i1 - i2) for i1, i2 in zip(sorted(list1), sorted(list2)))


def get_similarities(numbers):
    list1, list2 = transpose(numbers)
    count2 = Counter(list2)
    return sum(n * count2[n] for n in list1)


def run_tests():
    numbers = get_numbers_from_lines(
        """3   4
4   3
2   5
1   3
3   9
3   3"""
    )
    assert get_total_distance(numbers) == 11
    assert get_similarities(numbers) == 31


def get_solutions():
    numbers = get_numbers_from_file()
    print(get_total_distance(numbers) == 2815556)
    print(get_similarities(numbers) == 23927637)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
