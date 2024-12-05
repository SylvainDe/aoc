# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import collections

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_rule_from_string(string):
    a, b = string.split("|")
    return int(a), int(b)


def get_input_data_from_lines(string):
    part1, part2 = string.split("\n\n")
    part1 = [get_rule_from_string(s) for s in part1.splitlines()]
    part2 = [[int(n) for n in s.split(",")] for s in part2.splitlines()]
    return part1, part2


def get_input_data_from_file(file_path=top_dir + "resources/year2024_day5_input.txt"):
    with open(file_path) as f:
        return get_input_data_from_lines(f.read())


def get_full_ordering(rules, update):
    update = set(update)
    order = collections.defaultdict(set)
    for a, b in rules:
        if a in update and b in update:
            s = order[a]
            objects_to_add = set([b])
            while objects_to_add:
                b = objects_to_add.pop()
                if b not in s:
                    s.add(b)
                    objects_to_add.update(order[b])
    for p, dep in order.items():
        assert p not in dep
    return order


def is_in_order(update, rules):
    seen = set()
    full_order = get_full_ordering(rules, update)
    for p in update:
        expected_after = full_order[p]
        if seen.intersection(expected_after):
            return False
        seen.add(p)
    # TODO
    return True


def get_part1(rules, updates):
    return sum(up[len(up)//2] for up in updates if is_in_order(up, rules))


def run_tests():
    rules, updates = get_input_data_from_lines(
        """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""
    )
    print(get_part1(rules, updates) == 143)


def get_solutions():
    rules, updates = get_input_data_from_file()
    print(get_part1(rules, updates))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
