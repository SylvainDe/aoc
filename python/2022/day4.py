# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_ids_from_line(string):
    id1, id2 = string.split(",")
    return tuple(int(n) for n in id1.split("-") + id2.split("-"))


def get_ids_from_lines(string):
    return [get_ids_from_line(l) for l in string.splitlines()]


def get_ids_from_file(file_path="../../resources/year2022_day4_input.txt"):
    with open(file_path) as f:
        return get_ids_from_lines(f.read())


def nb_fully_contains(ids):
    return sum((a <= c <= d <= b) or (c <= a <= b <= d) for a, b, c, d in ids)


def nb_overlap(ids):
    return sum(a <= d and b >= c for a, b, c, d in ids)


def run_tests():
    ids = get_ids_from_lines(
        """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""
    )
    assert nb_fully_contains(ids) == 2
    assert nb_overlap(ids) == 4


def get_solutions():
    ids = get_ids_from_file()
    print(nb_fully_contains(ids) == 518)
    print(nb_overlap(ids) == 909)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
