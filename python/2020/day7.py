# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import re


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"

def get_rules_from_file(file_path=top_dir + "resources/year2020_day7_input.txt"):
    with open(file_path) as f:
        return [get_rule_from_line(l.strip()) for l in f]


color_desc = r"[a-z]+ [a-z]+"
rule_re = re.compile(r"(?P<container>" + color_desc + ") bags contain (?P<content>.*).")
content_re = re.compile(r"(?P<number>\d+) (?P<color>" + color_desc + ") bags?")


def get_rule_from_line(line):
    m = rule_re.fullmatch(line)
    assert m
    lst = []
    container, content = m.groups()
    if content != "no other bags":
        for content_item in content.split(", "):
            m2 = content_re.fullmatch(content_item)
            if m2:
                nb, color = m2.groups()
                lst.append((int(nb), color))
            else:
                print(content_item, "did not match")
    return container, lst


def get_nb_colors_to_contain(rules, color):
    can_be_in = dict()
    for c1, lst in rules:
        for _, c2 in lst:
            can_be_in.setdefault(c2, []).append(c1)

    reachable = set()
    to_process = set([color])
    while to_process:
        c1 = to_process.pop()
        reachable.add(c1)
        for c2 in can_be_in.get(c1, []):
            if c2 not in reachable:
                to_process.add(c2)
    return len(reachable) - 1


def get_number_of_bags_in_colored_bag(rules, color):
    computed_bags = dict()
    change = True
    while change:
        change = False
        for c1, lst in rules:
            if c1 not in computed_bags and all(c2 in computed_bags for _, c2 in lst):
                nb_bags = sum(nb * computed_bags[c2] for nb, c2 in lst)
                if c1 == color:
                    return nb_bags
                computed_bags[c1] = 1 + nb_bags
                change = True
    return None


def run_tests():
    assert get_rule_from_line(
        "light red bags contain 1 bright white bag, 2 muted yellow bags."
    ) == ("light red", [(1, "bright white"), (2, "muted yellow")])
    assert get_rule_from_line("faded blue bags contain no other bags.") == (
        "faded blue",
        [],
    )
    example1 = [
        "light red bags contain 1 bright white bag, 2 muted yellow bags.",
        "dark orange bags contain 3 bright white bags, 4 muted yellow bags.",
        "bright white bags contain 1 shiny gold bag.",
        "muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.",
        "shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.",
        "dark olive bags contain 3 faded blue bags, 4 dotted black bags.",
        "vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.",
        "faded blue bags contain no other bags.",
        "dotted black bags contain no other bags.",
    ]
    rules = [get_rule_from_line(l) for l in example1]
    assert get_nb_colors_to_contain(rules, "shiny gold") == 4
    assert get_number_of_bags_in_colored_bag(rules, "shiny gold") == 32

    example2 = [
        "shiny gold bags contain 2 dark red bags.",
        "dark red bags contain 2 dark orange bags.",
        "dark orange bags contain 2 dark yellow bags.",
        "dark yellow bags contain 2 dark green bags.",
        "dark green bags contain 2 dark blue bags.",
        "dark blue bags contain 2 dark violet bags.",
        "dark violet bags contain no other bags.",
    ]
    rules = [get_rule_from_line(l) for l in example2]
    assert get_number_of_bags_in_colored_bag(rules, "shiny gold") == 126


def get_solutions():
    rules = get_rules_from_file()
    print(get_nb_colors_to_contain(rules, "shiny gold") == 296)
    print(get_number_of_bags_in_colored_bag(rules, "shiny gold") == 9339)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
