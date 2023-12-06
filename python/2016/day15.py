# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import re
import collections
import itertools


resource_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../resources/"

# "Disc #1 has 13 positions; at time=0, it is at position 10."
disc_re = r"^Disc \#(?P<number>\d+) has (?P<nb_pos>\d+) positions; at time=0, it is at position (?P<init_pos>\d+).$"

Disc = collections.namedtuple("Disc", ("number", "nb_positions", "initial_position"))


def get_disc_from_str(s):
    match = re.match(disc_re, s)
    d = match.groupdict()
    return Disc(int(d["number"]), int(d["nb_pos"]), int(d["init_pos"]))


def get_discs_from_file(file_path=resource_dir + "year2016_day15_input.txt"):
    with open(file_path) as f:
        return [get_disc_from_str(l.strip()) for l in f]


def goes_through(discs, time):
    return all(
        (d.number + d.initial_position + time) % d.nb_positions == 0 for d in discs
    )


def get_press_time(discs):
    # There must be a smarter way involving modular arithmetic
    for i in itertools.count():
        if goes_through(discs, i):
            return i


def run_tests():
    discs = [
        "Disc #1 has 5 positions; at time=0, it is at position 4.",
        "Disc #2 has 2 positions; at time=0, it is at position 1.",
    ]
    discs = [get_disc_from_str(s) for s in discs]
    assert not goes_through(discs, 0)
    assert not goes_through(discs, 1)
    assert not goes_through(discs, 2)
    assert not goes_through(discs, 3)
    assert not goes_through(discs, 4)
    assert goes_through(discs, 5)
    assert get_press_time(discs) == 5


def get_solutions():
    discs = get_discs_from_file()
    print(get_press_time(discs) == 203660)
    new_number = max(d.number for d in discs) + 1
    discs2 = discs + [Disc(new_number, 11, 0)]
    print(get_press_time(discs2) == 2408135)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
