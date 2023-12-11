# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import itertools
import re
import functools
import math

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


def get_steps_to_reach(instr, nodes, begin, ends):
    pos = begin
    for i in itertools.cycle(instr):
        if pos in ends:
            return
        yield pos
        left, right = nodes[pos]
        pos = left if i == 'L' else right

def get_nb_steps_part1(instr, nodes):
    return len(list(get_steps_to_reach(instr, nodes, "AAA", {"ZZZ"})))

def get_steps_to_reach_ghost_naive(instr, nodes, begin="A", end="Z"):
    pos = {n for n in nodes if n.endswith(begin)}
    for i in itertools.cycle(instr):
        if all(p.endswith(end) for p in pos):
            return
        yield pos
        idx = 0 if i == 'L' else 1
        pos = {nodes[p][idx] for p in pos}

def lcm(a, b):
    """Computes lcm for 2 numbers."""
    return a * b // math.gcd(a, b)


def lcmm(*args):
    """Computes lcm for numbers."""
    return functools.reduce(lcm, args)

def get_nb_steps_to_reach_ghost(instr, nodes, begin="A", end="Z"):
    ends = {n for n in nodes if n.endswith(end)}
    nb_steps = {
        len(list(get_steps_to_reach(instr, nodes, n, ends)))
        for n in nodes
        if n.endswith(begin)
    }
    return lcmm(*nb_steps)


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
    assert get_nb_steps_part1(instr, nodes) == 2
    instr, nodes = get_data_from_lines(
        """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""
    )
    assert get_nb_steps_part1(instr, nodes) == 6
    instr, nodes = get_data_from_lines(
        """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""
    )
    assert len(list(get_steps_to_reach_ghost_naive(instr, nodes))) == 6
    assert get_nb_steps_to_reach_ghost(instr, nodes) == 6


def get_solutions():
    instr, nodes = get_data_from_file()
    print(get_nb_steps_part1(instr, nodes) == 19637)
    print(get_nb_steps_to_reach_ghost(instr, nodes) == 8811050362409)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
