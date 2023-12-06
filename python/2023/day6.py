# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import functools
import operator
import math

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
    # (time - button) * button > distance)
    # button² - time*button + distance < 0
    # delta = time² - 4distance
    # x1 = (time - sqrt(delta))/ 2 ; x2 = (time + sqrt(delta))/ 2
    delta = time * time - 4 * distance
    if delta < 0:
        return 0
    sq = math.sqrt(delta)
    x1 = (time - sq) / 2
    x2 = (time + sq) / 2
    perfect_sq = (int(sq)**2 == delta)
    return math.floor(x2) - math.ceil(x1) + (-1 if perfect_sq else 1)

def get_nb_winning_ways_product(races):
    return mult(get_nb_winning_ways(r) for r in races)

def get_new_race(races):
    time = int("".join(str(t) for t, _ in races))
    dist = int("".join(str(d) for _, d in races))
    return (time, dist)

def run_tests():
    races = get_races_from_lines(
        """Time:      7  15   30
Distance:  9  40  200"""
    )
    assert get_nb_winning_ways_product(races) == 288
    assert get_nb_winning_ways(get_new_race(races)) == 71503

def get_solutions():
    races = get_races_from_file()
    print(get_nb_winning_ways_product(races) == 625968)
    print(get_nb_winning_ways(get_new_race(races)) == 43663323)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
