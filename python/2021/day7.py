# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import math


def get_crabs_from_file(file_path="day7_input.txt"):
    with open(file_path) as f:
        for l in f:
            return [int(v) for v in l.strip().split(",")]


def dist1(pos1, pos2):
    return abs(pos1 - pos2)


def dist2(pos1, pos2):
    d = dist1(pos1, pos2)
    return d * (d + 1) // 2


def cost(crabs, pos, func):
    return sum(func(pos, crab) for crab in crabs)


def min_cost(crabs, func, positions_to_consider):
    return min(cost(crabs, p, func) for p in positions_to_consider)


def get_best_position_dist1(crabs):
    crabs = sorted(crabs)
    n = len(crabs)
    # Get cost around median position
    positions = (crabs[n // 2], crabs[(n + 1) // 2])
    return min_cost(crabs, dist1, positions)


def get_best_position_dist2(crabs):
    # 1. Computing the minimal cost with a square cost: C = d²
    #    can be done:
    #       F(x) = (p1 - x)² + (p2 - x)² + ... + (pn - x)²
    #       F(x) = nx² - 2x(p1 + p2 + ... + pn) + (p1² + p2² + ... + pn²)
    #       F²(x) = 2nx - 2(p1 + p2 + ... + pn)
    #       F'(x) = 0 <=> x = (p1 + ... + pn) / n
    #
    # 2. Moving d cost C = (d+1)*d/2 which is slightly trickier to
    #    optimise as it involves computing absolute values.
    # 3. Using the best solution for problem 1 works for problem 2 but I don't know why
    avg = sum(crabs) / len(crabs)
    positions = (math.floor(avg), math.ceil(avg))
    return min_cost(crabs, dist2, positions)


def run_tests():
    crabs = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
    assert get_best_position_dist1(crabs) == 37
    assert get_best_position_dist2(crabs) == 168


def get_solutions():
    crabs = get_crabs_from_file()
    print(get_best_position_dist1(crabs))
    print(get_best_position_dist2(crabs))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
