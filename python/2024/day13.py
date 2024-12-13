# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import re
import math

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


input_re = (
    r"Button A: X\+(\d+), Y\+(\d+)-Button B: X\+(\d+), Y\+(\d+)-Prize: X=(\d+), Y=(\d+)"
)


def get_machines_from_lines(string):
    for s in string.split("\n\n"):
        s = s.replace("\n", "-")
        ax, ay, bx, by, px, py = [int(v) for v in re.match(input_re, s).groups()]
        yield (ax, ay), (bx, by), (px, py)


def get_machines_from_file(file_path=top_dir + "resources/year2024_day13_input.txt"):
    with open(file_path) as f:
        return get_machines_from_lines(f.read())


def xgcd(a, b, s1=1, s2=0, t1=0, t2=1):
    """Calculates the gcd and Bezout coefficients,
    using the Extended Euclidean Algorithm (recursive).
    (Source: extendedeuclideanalgorithm.com/code)
    """
    if b == 0:
        return abs(a), 1, 0

    q = math.floor(a / b)
    r = a - q * b
    s3 = s1 - q * s2
    t3 = t1 - q * t2

    # if r==0, then b will be the gcd and s2, t2 the Bezout coefficients
    return (abs(b), s2, t2) if (r == 0) else xgcd(b, r, s2, s3, t2, t3)


def det(a, b, c, d):
    return a * d - b * c


def get_min_spend_for_machine(m, part1):
    (ax, ay), (bx, by), (px, py) = m
    # ax * A + bx * B = px   (eq 1)
    # ay * A + by * B = py   (eq 2)
    # min(3*A+B)
    # https://en.wikipedia.org/wiki/Cramer%27s_rule
    if not part1:
        error = 10000000000000
        px += error
        py += error
    detm = det(ax, bx, ay, by)
    deta = det(px, bx, py, by)
    detb = det(ax, px, ay, py)
    a, b = deta / detm, detb / detm
    a, b = int(a), int(b)
    if a < 0 or b < 0 or ax * a + bx * b != px:
        return 0
    if part1:
        max_press = 100
        if a > max_press or b > max_press:
            return 0
    return 3 * a + b


def get_min_spend(machines, part1=True):
    return sum(get_min_spend_for_machine(m, part1) for m in machines)


def run_tests():
    machines = list(
        get_machines_from_lines(
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
        )
    )
    assert get_min_spend(machines) == 480


def get_solutions():
    machines = list(get_machines_from_file())
    print(get_min_spend(machines) == 29438)
    print(get_min_spend(machines, False) == 104958599303720)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
