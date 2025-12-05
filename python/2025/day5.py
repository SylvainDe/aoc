# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_range_from_string(string):
    a, b = string.split("-")
    return (int(a), int(b))


def get_db_from_lines(string):
    fresh_ranges, avail = string.split("\n\n")
    return [get_range_from_string(r) for r in fresh_ranges.splitlines()], [int(i) for i in avail.splitlines()]


def get_db_from_file(file_path=top_dir + "resources/year2025_day5_input.txt"):
    with open(file_path) as f:
        return get_db_from_lines(f.read())


def is_fresh(ing, fresh_ranges):
    for a, b in fresh_ranges:
        if a <= ing <= b:
            return True
    return False


def get_fresh_available_ingredients(db):
    fresh_ranges, avail = db
    return [i for i in avail if is_fresh(i, fresh_ranges)]


def get_nb_fresh_ingredients_naive(fresh_ranges):
    return len(set(i for a, b in fresh_ranges for i in range(a, b+1)))


def get_union_ranges(ranges):
    union = set()
    ranges = set(ranges)
    while ranges:
        r1 = ranges.pop()
        beg1, end1 = r1
        assert beg1 <= end1
        for r2 in union:
            beg2, end2 = r2
            assert beg2 <= end2
            if end1 >= beg2 and end2 >= beg1:
                union.remove(r2)
                ranges.add((min(beg1, beg2), max(end1, end2)))
                break
        else:
            union.add(r1)
    return union



def get_nb_fresh_ingredients(fresh_ranges):
    return sum(1 + b - a for a, b in get_union_ranges(fresh_ranges))


def run_tests():
    db = get_db_from_lines(
        """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""
    )
    assert len(get_fresh_available_ingredients(db)) == 3
    fresh_ranges, _ = db
    assert get_nb_fresh_ingredients_naive(fresh_ranges) == 14
    assert get_nb_fresh_ingredients(fresh_ranges) == 14


def get_solutions():
    db = get_db_from_file()
    print(len(get_fresh_available_ingredients(db)) == 525)
    fresh_ranges, _ = db
    print(get_nb_fresh_ingredients(fresh_ranges) == 333892124923577)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
