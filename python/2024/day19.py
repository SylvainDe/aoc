# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_towel_input_from_lines(string):
    beg, mid, end = string.partition("\n\n")
    return [beg.split(", "), end.splitlines()]


def get_towel_input_from_file(file_path=top_dir + "resources/year2024_day19_input.txt"):
    with open(file_path) as f:
        return get_towel_input_from_lines(f.read())


def can_be_reached(onsen, patterns):
    if not onsen:
        return True
    for p in patterns:
        if onsen.startswith(p) and can_be_reached(onsen[len(p) :], patterns):
            return True
    return False


def simplify_patterns(patterns):
    reachable = set(
        p for p in patterns if can_be_reached(p, [p2 for p2 in patterns if p2 != p])
    )
    new_patterns = [p for p in patterns if p not in reachable]
    for p in reachable:
        assert can_be_reached(p, new_patterns)
    return new_patterns


def part1(towel_input):
    patterns, onsen = towel_input
    new_patterns = simplify_patterns(patterns)
    return sum(can_be_reached(o, [p for p in new_patterns if p in o]) for o in onsen)


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


def get_solutions():
    towel_input = get_towel_input_from_file()
    print(part1(towel_input) == 278)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
