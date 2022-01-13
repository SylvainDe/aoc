# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import re

left_re = r"(.*) \((\d+)\)"


def get_program_from_string(s):
    left, mid, right = s.partition(" -> ")
    lst = right.split(", ") if right else []
    name, weight = re.match(left_re, left).groups()
    return name, int(weight), lst


def get_prog_from_file(file_path="day7_input.txt"):
    with open(file_path) as f:
        return [get_program_from_string(l.strip()) for l in f]


def get_bottom(programs):
    parents = dict()
    for name, _, lst in programs:
        for e in lst:
            assert e not in parents
            parents[e] = name
    bottoms = [name for name, _, lst in programs if name not in parents]
    assert len(bottoms) == 1
    return bottoms[0]


def run_tests():
    prog = [
        "pbga (66)",
        "xhth (57)",
        "ebii (61)",
        "havc (66)",
        "ktlj (57)",
        "fwft (72) -> ktlj, cntj, xhth",
        "qoyq (66)",
        "padx (45) -> pbga, havc, qoyq",
        "tknk (41) -> ugml, padx, fwft",
        "jptl (61)",
        "ugml (68) -> gyxo, ebii, jptl",
        "gyxo (61)",
        "cntj (57)",
    ]
    prog = [get_program_from_string(s) for s in prog]
    assert get_bottom(prog) == "tknk"


def get_solutions():
    prog = get_prog_from_file()
    print(get_bottom(prog))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
