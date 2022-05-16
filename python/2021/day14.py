# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import collections


def get_pair_insertion_rules(line, sep=" -> "):
    left, mid, right = line.partition(sep)
    assert mid == sep
    return (tuple(left), right)


def get_info_from_lines(lines):
    lines = [line.strip() for line in lines]
    template, remaining = lines[0], lines[2:]
    rules = dict(get_pair_insertion_rules(line) for line in remaining)
    return template, rules


def get_info_from_file(file_path="day14_input.txt"):
    with open(file_path) as f:
        return get_info_from_lines(f)


def perform_step(template, rules):
    ret = [template[0]]
    for c1, c2 in zip(template, template[1:]):
        insert = rules.get((c1, c2), None)
        if insert is not None:
            ret.append(insert)
        ret.append(c2)
    return "".join(ret)


def perform_steps(template, rules, steps):
    for i in range(steps):
        template = perform_step(template, rules)
    return template


def get_quantity(template, rules, steps):
    template = perform_steps(template, rules, steps)
    commons = collections.Counter(template).most_common()
    return commons[0][1] - commons[-1][1]


def get_fast_quantity(template, rules, steps):
    rules2 = {(a, b): ((a, i), (i, b)) for (a, b), i in rules.items()}
    pairs = collections.Counter(zip(template, template[1:]))
    for i in range(steps):
        pairs2 = collections.Counter()
        for pair, count in pairs.items():
            for pair2 in rules2.get(pair, [pair]):
                pairs2[pair2] += count
        pairs = pairs2
    letter_count = collections.Counter(template) - collections.Counter(template[1:-1])
    for (a, b), count in pairs.items():
        letter_count[a] += count
        letter_count[b] += count
    assert len(template) < 2 or all(count % 2 == 0 for count in letter_count.values())
    commons = letter_count.most_common()
    return (commons[0][1] // 2) - (commons[-1][1] // 2)


def run_tests():
    info = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C""".splitlines()
    template, rules = get_info_from_lines(info)
    assert (
        perform_steps(template, rules, 4)
        == "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB"
    )
    assert get_quantity(template, rules, 10) == 1588
    assert get_fast_quantity(template, rules, 10) == 1588
    for t in [template, "N", "NN", "NNN", "HH", "HHH", "HHHH", "CB", "XX"]:
        for n in range(11):
            fast = get_fast_quantity(t, rules, n)
            slow = get_quantity(t, rules, n)
            assert fast == slow


def get_solutions():
    template, rules = get_info_from_file()
    print(get_quantity(template, rules, 10))
    print(get_fast_quantity(template, rules, 40))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
