# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import itertools


def get_numbers(file_path="../../resources/year2020_day1_input.txt"):
    with open(file_path) as f:
        return set(int(l) for l in f)


# Note: various optimisations possible, in particular for day1_part2.
# This would get more relevant with bigger inputs or if one wants all
# solutions without assuming that there is only one.
# For instance, one could consider looking for n1 < n2 < n3 which gives
# an early exit condition for each loop level.


def day1_part1(nbs, target_sum=2020):
    for n1 in nbs:
        n2 = target_sum - n1
        if n2 in nbs:
            return n1 * n2


def day1_part2(nbs, target_sum=2020):
    for n1, n2 in itertools.combinations(nbs, 2):
        n3 = target_sum - n1 - n2
        if n3 in nbs:
            return n1 * n2 * n3


def run_tests():
    nbs = set((1721, 979, 366, 299, 675, 1456))
    assert day1_part1(nbs) == 514579
    assert day1_part2(nbs) == 241861950


def get_solutions():
    nbs = get_numbers()
    print(day1_part1(nbs) == 73371)
    print(day1_part2(nbs) == 127642310)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
