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


def get_min_spend_for_machine(m, part1, max_press=100, error=10000000000000):
    (ax, ay), (bx, by), (px, py) = m
    # ax * A + bx * B = px   (eq 1)
    # ay * A + by * B = py   (eq 2)
    # min(3*A+B)
    # TODO: https://en.wikipedia.org/wiki/B%C3%A9zout%27s_identity
    mini = 0
    if part1:
        for a in range(max_press):
            for b in range(max_press):
                if ax * a + bx * b == px and ay * a + by * b == py:
                    c = 3 * a + b
                    if mini == 0 or mini > c:
                        mini = c
    else:
        # TODO
        # px += error
        # py += error
        gcdx, cax, cbx = xgcd(ax, bx)
        gcdy, cay, cby = xgcd(ay, by)
        qx, rx = divmod(px, gcdx)
        qy, ry = divmod(py, gcdy)
        assert ax * cax + bx * cbx == gcdx
        assert ay * cay + by * cby == gcdy
        if rx == 0 and ry == 0:
            cax *= qx
            cbx *= qx
            cay *= qy
            cby *= qy
            assert ax * cax + bx * cbx == px
            assert ay * cay + by * cby == py
            incax, incbx = -bx // gcdx, ax // gcdx
            incay, incby = -by // gcdy, ay // gcdy
            # Solutions for (1) are: (cax - k*incax, cbx+k*incbx)
            # Solutions for (2) are: (cay - k*incay, cby+k*incby)
            for k in [-100, -10, -1, 0, 1, 10, 100]:
                assert ax * (cax + k * incax) + bx * (cbx + k * incbx) == px
                assert ay * (cay + k * incay) + by * (cby + k * incby) == py
            # But we also want:
            #  A = cax + kx*incax = cay + ky*incay
            #  B = cbx + kx*incbx = cby + ky*incby
            # Did we replace a system of equation by another one just as hard?
            if px == 8400:
                A, B = 80, 40
                kx, ky = 1520, 160
                assert ax * A + bx * B == px
                assert ay * A + by * B == py
                assert A == cax + kx * incax
                assert B == cbx + kx * incbx
                assert A == cay + ky * incay
                assert B == cby + ky * incby
    return mini


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
    print(get_min_spend(machines, False))


def get_solutions():
    machines = list(get_machines_from_file())
    print(get_min_spend(machines) == 29438)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
