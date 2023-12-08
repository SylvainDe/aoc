# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import itertools
import re

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


NODE_RE = re.compile(r"(\w+) = \((\w+), (\w+)\)")


def get_node_from_line(string):
    m = NODE_RE.match(string)
    begin, left, right = m.groups()
    return begin, (left, right)


def get_data_from_lines(string):
    lst = string.splitlines()
    return lst[0], dict(get_node_from_line(l) for l in lst[2:])


def get_data_from_file(file_path=top_dir + "resources/year2023_day8_input.txt"):
    with open(file_path) as f:
        return get_data_from_lines(f.read())


def get_steps_to_reach(instr, nodes, begin="AAA", end="ZZZ"):
    pos = begin
    for i in itertools.cycle(instr):
        if pos == end:
            return
        yield pos
        left, right = nodes[pos]
        pos = left if i == 'L' else right

def run_tests():
    instr, nodes = get_data_from_lines(
        """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""
    )
    assert len(list(get_steps_to_reach(instr, nodes))) == 2
    instr, nodes = get_data_from_lines(
        """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""
    )
    assert len(list(get_steps_to_reach(instr, nodes))) == 6


def get_solutions():
    instr, nodes = get_data_from_file()
    print(len(list(get_steps_to_reach(instr, nodes))) == 19637)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
