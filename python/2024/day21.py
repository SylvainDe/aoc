# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import itertools
import functools

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_codes_from_lines(string):
    return string.splitlines()


def get_codes_from_file(file_path=top_dir + "resources/year2024_day21_input.txt"):
    with open(file_path) as f:
        return get_codes_from_lines(f.read())


def keypad_buttons(keypad):
    for i, l in enumerate(keypad.splitlines()):
        for j, v in enumerate(l):
            if v != "X":
                yield (i, j), v


def get_shortest_move(p1, p2, valid_pos):
    # To go from one button to another, we assume that
    # only at most 2 paths are going to be relevant:
    #  - horizontal (</>) then vertical (^/v)
    #  - vertical (^/v) then horizontal (</>)
    # as mixing does not seem efficient
    #
    # This means changing direction once and in (at most)
    # 2 possible places:
    #  - (x2, y1) for the vertical move
    #  - (x1, y2) for the horizontal move
    # and under the condition that this position is valid
    #
    # Finally, we have multiple combinations and for some
    # reason:
    # "<vA" is better than "v<A"
    # "<^A" is better than "^<A"
    # "^>A" is better than ">^A"
    # "v>A" is better than ">vA"
    x1, y1 = p1
    x2, y2 = p2
    dx, dy = x2 - x1, y2 - y1
    x_buttons = ("v" if dx > 0 else "^") * abs(dx)
    y_buttons = (">" if dy > 0 else "<") * abs(dy)
    x_first = True
    if dx and dy:
        mx, my = (x2, y1), (x1, y2)
        if my not in valid_pos:
            x_first = True
        elif mx not in valid_pos:
            x_first = False
        elif dy < 0:
            x_first = False
    return (x_buttons + y_buttons) if x_first else (y_buttons + x_buttons)


def precompute_shortest_moves(keypad):
    keypad = list(keypad)
    valid_pos = set(pos for pos, _ in keypad)
    return {
        (c1, c2): get_shortest_move(p1, p2, valid_pos) + "A"
        for (p1, c1), (p2, c2) in itertools.product(keypad, repeat=2)
    }


num_shortest_move = precompute_shortest_moves(keypad_buttons("789\n456\n123\nX0A"))
dir_shortest_move = precompute_shortest_moves(keypad_buttons("X^A\n<v>"))


def shortest_seq(code, precomputed, start="A"):
    return "".join(precomputed[(c1, c2)] for c1, c2 in zip(start + code, code))


def get_shortest_seq_len_iter(code, nb_robot_direct_keypad):
    seq = shortest_seq(code, num_shortest_move)
    for n in range(nb_robot_direct_keypad):
        seq = shortest_seq(seq, dir_shortest_move)
    return len(seq)


@functools.lru_cache
def get_shortest_seq_len_rec(code, nb_robot_direct_keypad):
    if nb_robot_direct_keypad == 0:
        return len(code)
    codes = [c + "A" for c in code.split("A")[:-1]]
    assert "".join(codes) == code
    return sum(
        get_shortest_seq_len_rec(
            shortest_seq(c, dir_shortest_move), nb_robot_direct_keypad - 1
        )
        for c in codes
    )


def get_shortest_seq_len(code, nb_robot_direct_keypad):
    return get_shortest_seq_len_rec(
        shortest_seq(code, num_shortest_move), nb_robot_direct_keypad
    )


def get_numeric_part(code):
    return int(code[:-1])


def get_complexity(code, nb_robot_direct_keypad):
    return get_shortest_seq_len(code, nb_robot_direct_keypad) * get_numeric_part(code)


def get_complexity_sum(codes, nb_robot_direct_keypad=2):
    return sum(get_complexity(c, nb_robot_direct_keypad) for c in codes)


def run_tests():
    codes = get_codes_from_lines(
        """029A
980A
179A
456A
379A"""
    )
    assert get_complexity_sum(codes) == 126384


def get_solutions():
    codes = get_codes_from_file()
    print(get_complexity_sum(codes) == 105458)
    print(get_complexity_sum(codes, 25) == 129551515895690)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
