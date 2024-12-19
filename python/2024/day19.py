# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import functools


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_towel_input_from_lines(string):
    beg, mid, end = string.partition("\n\n")
    return [beg.split(", "), end.splitlines()]


def get_towel_input_from_file(file_path=top_dir + "resources/year2024_day19_input.txt"):
    with open(file_path) as f:
        return get_towel_input_from_lines(f.read())


@functools.lru_cache
def can_be_reached(onsen, patterns):
    if not onsen:
        return True
    return any(
        onsen.startswith(p) and can_be_reached(onsen[len(p) :], patterns)
        for p in patterns
    )


@functools.lru_cache
def nb_ways(onsen, patterns):
    if not onsen:
        return 1
    return sum(
        onsen.startswith(p) and nb_ways(onsen[len(p) :], patterns) for p in patterns
    )


def part1(towel_input):
    patterns, onsen = towel_input
    patterns = tuple(patterns)
    return sum(can_be_reached(o, patterns) for o in onsen)


def part2(towel_input):
    patterns, onsen = towel_input
    patterns = tuple(patterns)
    return sum(nb_ways(o, patterns) for o in onsen)


def run_tests():
    towel_input = get_towel_input_from_lines(
        """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""
    )
    assert part1(towel_input) == 6
    assert part2(towel_input) == 16


def get_solutions():
    towel_input = get_towel_input_from_file()
    print(part1(towel_input) == 278)
    print(part2(towel_input) == 569808947758890)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
