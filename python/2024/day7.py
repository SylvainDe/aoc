# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_equation_from_line(string):
    val, nbs = string.split(": ")
    return int(val), [int(n) for n in nbs.split()]


def get_equations_from_lines(string):
    return [get_equation_from_line(l) for l in string.splitlines()]


def get_equations_from_file(file_path=top_dir + "resources/year2024_day7_input.txt"):
    with open(file_path) as f:
        return get_equations_from_lines(f.read())


def can_be_reached(val, nbs, part2):
    if not nbs:
        return val == 0
    begin, end = nbs[:-1], nbs[-1]
    d = val - end
    if d >= 0 and can_be_reached(d, begin, part2):
        return True
    q, r = divmod(val, end)
    if r == 0 and can_be_reached(q, begin, part2):
        return True
    if part2:
        val_str = str(val)
        end_str = str(end)
        if val_str.endswith(end_str):
            return can_be_reached(int(val_str[: -len(end_str)]), begin, part2)
    return False


def get_reachable_nb_sum(equations, part2=False):
    return sum(val for val, nbs in equations if can_be_reached(val, nbs, part2))


def run_tests():
    equations = get_equations_from_lines(
        """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""
    )
    assert get_reachable_nb_sum(equations) == 3749
    assert get_reachable_nb_sum(equations, True) == 11387


def get_solutions():
    equations = get_equations_from_file()
    print(get_reachable_nb_sum(equations) == 2664460013123)
    print(get_reachable_nb_sum(equations, True) == 426214131924213)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
