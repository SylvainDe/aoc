# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


resource_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../resources/"


def get_data_from_file(file_path=resource_dir + "year2020_day19_input.txt"):
    with open(file_path) as f:
        rules, strings = f.read().split("\n\n")
        return get_rules_from_string(rules), strings.splitlines()


quote = '"'
pipe = " | "


def get_rule_from_string(string):
    left, right = string.split(": ")
    left = int(left)
    if right.startswith(quote):
        assert right.endswith(quote)
        return left, right[1:-1]
    alternatives = right.split(pipe)
    return left, [[int(n) for n in alt.split()] for alt in alternatives]


def get_rules_from_string(string):
    rules = dict()
    for l in string.splitlines():
        n, r = get_rule_from_string(l)
        rules[n] = r
    return rules


def seq_match_string(rules, seq, s):
    if not seq:
        yield s
    else:
        head, tail = seq[0], seq[1:]
        for rem in rule_match_string(rules, head, s):
            yield from seq_match_string(rules, tail, rem)


def rule_match_string(rules, rule_nb, s):
    rule = rules[rule_nb]
    # Either a literal string
    if isinstance(rule, str):
        if s.startswith(rule):
            yield s[len(rule) :]
    # Or a list of alternatives
    else:
        for alt in rule:
            yield from seq_match_string(rules, alt, s)


def rules_match_string(rules, s):
    return "" in rule_match_string(rules, 0, s)


def example1():
    rules = """0: 1 2
1: "a"
2: 1 3 | 3 1
3: "b\""""
    rules = get_rules_from_string(rules)
    for s in ["aab", "aba"]:
        assert rules_match_string(rules, s)
    for s in ["aaa"]:
        assert not rules_match_string(rules, s)


def example2():
    rules = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b\""""
    rules = get_rules_from_string(rules)
    for s in [
        "aaaabb",
        "aaabab",
        "abbabb",
        "abbbab",
        "aabaab",
        "aabbbb",
        "abaaab",
        "ababbb",
    ]:
        assert rules_match_string(rules, s)
    for s in [
        "aaaabba",
        "aaababb",
        "abbbbb",
        "aabbab",
        "baabaab",
        "aaabbb",
        "ababab",
        "abaabbb",
    ]:
        assert not rules_match_string(rules, s)


def run_tests():
    example1()
    example2()


def get_solutions():
    rules, strings = get_data_from_file()
    print(sum(rules_match_string(rules, s) for s in strings) == 118)
    new_rules = [
        "8: 42 | 42 8",
        "11: 42 31 | 42 11 31",
    ]
    for line in new_rules:
        n, r = get_rule_from_string(line)
        rules[n] = r
    print(sum(rules_match_string(rules, s) for s in strings) == 246)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
