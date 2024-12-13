# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import re
import math

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


input_re = r"Button A: X\+(\d+), Y\+(\d+)-Button B: X\+(\d+), Y\+(\d+)-Prize: X=(\d+), Y=(\d+)"


def get_machines_from_lines(string):
    for s in string.split("\n\n"):
        s = s.replace("\n", "-")
        ax, ay, bx, by, px, py = [int(v) for v in re.match(input_re, s).groups()]
        yield (ax, ay), (bx, by), (px, py)

def get_machines_from_file(file_path=top_dir + "resources/year2024_day13_input.txt"):
    with open(file_path) as f:
        return get_machines_from_lines(f.read())


def get_min_spend_for_machine(m, max_press):
    (ax, ay), (bx, by), (px, py) = m
    # ax * A + bx * B = px
    # ay * A + by * B = py
    # min(3*A B)
    # TODO: https://en.wikipedia.org/wiki/B%C3%A9zout%27s_identity
    mini = 0
    for a in range(max_press):
        for b in range(max_press):
            if ax * a + bx * b == px and ay * a + by * b == py:
                c = 3 * a + b
                if mini == 0 or mini > c:
                    mini = c
    return mini

def get_min_spend(machines, max_press=100):
    return sum(get_min_spend_for_machine(m, max_press) for m in machines)


def run_tests():
    machines = list(get_machines_from_lines(
        """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""
    ))
    assert get_min_spend(machines) == 480

def get_solutions():
    machines = list(get_machines_from_file())
    print(get_min_spend(machines))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
