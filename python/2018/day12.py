# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_initial_state_from_line(string):
    return set(i for i, val in enumerate(string.split(" ")[2]) if val == "#")


def get_transition_from_line(string):
    sep = " => "
    beg, mid, end = string.partition(sep)
    assert mid == sep
    return beg, end


def get_full_input_from_lines(string):
    init, trans = string.split("\n\n")
    return get_initial_state_from_line(init), dict(
        get_transition_from_line(l) for l in trans.splitlines()
    )


def get_full_input_from_file(file_path=top_dir + "resources/year2018_day12_input.txt"):
    with open(file_path) as f:
        return get_full_input_from_lines(f.read())


def bool_to_char(val):
    return "#" if val else "."


def print_state(state, val_range=None):
    if val_range is None:
        if not state:
            val_range = ()
        else:
            val_range = range(min(state), max(state) + 1)
    state_str = (
        "".join(bool_to_char(val in state) for val in val_range) + " " + str(state)
    )
    # print(state_str)
    return state_str


def next_state(i, state, transitions, side_len):
    neighbours = "".join(
        bool_to_char(j in state) for j in range(i - side_len, i + side_len + 1)
    )
    ret = transitions.get(neighbours, ".")
    return ret


def next_gen(state, transitions, side_len=2):
    assert transitions.get("...", ".") == "."
    if not state:
        return state
    return set(
        i
        for i in range(min(state) - side_len, max(state) + side_len + 1)
        if next_state(i, state, transitions, side_len) == "#"
    )


def n_th_generation(state, transitions, n):
    for i in range(n):
        state = next_gen(state, transitions)
    return sum(state)


def run_tests():
    init, trans = get_full_input_from_lines(
        """initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #"""
    )
    assert n_th_generation(init, trans, 20) == 325


def get_solutions():
    init, trans = get_full_input_from_file()
    print(n_th_generation(init, trans, 20) == 3421)
    # After a while, the configuration is stabilized and just shifts toward the right.
    # Hence, the sum gets increased by a same amount (which is the number of pot) at
    # each generation as each pot value gets increased by one.
    # After stabilisation: S(n) = a * n + b
    x1, x2 = 199, 200
    y1, y2 = (n_th_generation(init, trans, x) for x in (x1, x2))
    a = (y1 - y2) / (x1 - x2)
    b = y1 - a * x1
    x3 = 50000000000
    print(a * x3 + b == 2550000001195)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
