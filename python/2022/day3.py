# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_rucksacks_from_file(file_path="../../resources/year2022_day3_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]

def get_prio(char):
    if char.islower():
        return ord(char) - ord('a') + 1
    if char.isupper():
        return ord(char) - ord('A') + 27
    assert False


def get_set_prio(sets):
    intersect = set.intersection(*sets)
    assert len(intersect) == 1
    return get_prio(intersect.pop())


def double_compartment_priority(rucksack):
    l = len(rucksack)
    q, r = divmod(l, 2)
    assert r == 0
    s1, s2 = rucksack[:q], rucksack[q:]
    assert len(s1) == len(s2) == q
    assert rucksack == s1 + s2
    return get_set_prio((set(s1), s2))


def part1(rucksacks):
   return sum(double_compartment_priority(r) for r in rucksacks)


def part2(rucksacks):
    # Inspired from itertools recipes
    args = [iter(rucksacks)] * 3
    return sum(get_set_prio((set(s1), s2, s3)) for (s1, s2, s3) in zip(*args))


def run_tests():
    rucksacks = ""


def get_solutions():
    rucksacks = get_rucksacks_from_file()
    print(part1(rucksacks) == 7889)
    print(part2(rucksacks) == 2825)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
