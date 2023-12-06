# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import functools
import operator

def mult(iterable, start=1):
    """Returns the product of an iterable - like the sum builtin."""
    return functools.reduce(operator.mul, iterable, start)

def get_races_from_lines(string):
    d = dict()
    for s in string.splitlines():
        beg, mid, end = s.partition(":")
        assert mid == ":"
        d[beg] = [int(s) for s in end.split()]
    return list(zip(d["Time"], d["Distance"]))


def get_races_from_file(file_path="../../resources/year2023_day6_input.txt"):
    with open(file_path) as f:
        return get_races_from_lines(f.read())


def get_nb_winning_ways(race):
    time, distance = race
    # Note: this could be determined with a bit of math and no loop
    return sum(((time - button) * button > distance) for button in range(time + 1))


def get_nb_winning_ways_product(races):
    return mult(get_nb_winning_ways(r) for r in races)


def run_tests():
    races = get_races_from_lines(
        """Time:      7  15   30
Distance:  9  40  200"""
    )
    assert get_nb_winning_ways_product(races) == 288

def get_solutions():
    races = get_races_from_file()
    print(get_nb_winning_ways_product(races) == 625968)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
