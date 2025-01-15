# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_codes_from_lines(string):
    return [l for l in string.splitlines()]


def get_codes_from_file(file_path=top_dir + "resources/year2024_day21_input.txt"):
    with open(file_path) as f:
        return get_codes_from_lines(f.read())


def keypad_buttons(keypad):
    for i, l in enumerate(keypad):
        for j, v in enumerate(l):
            if True or v != "X":
                yield v, (i, j)


num_keypad = dict(
    keypad_buttons(
        [
            "789",
            "456",
            "123",
            "X0A",
        ]
    )
)


dir_keypad = dict(
    keypad_buttons(
        [
            "X^A",
            "<v>",
        ]
    )
)

dir_to_key = {
    (-1, 0): "^",
    (1, 0): "v",
    (0, -1): "<",
    (0, 1): ">",
}


def keys_from_delta(val, direc):
    if not val:
        return ""
    x, y = direc
    abs_val = abs(val)
    q = val // abs_val
    return dir_to_key[(x * q, y * q)] * abs_val


# For the time being, assume that starting with a
# horizontal move is better
y_move_first = True


def shortest_sequence(code, keypad):
    seq = ""
    invalid_pos = keypad["X"]
    pos = [keypad[c] for c in "A" + code]
    for (prev_x, prev_y), (x, y) in zip(pos, pos[1:]):
        dx, dy = x - prev_x, y - prev_y
        # To go from one button to another, we assume that
        # only at most 2 paths are going to be relevant:
        #  - horizontal (</>) then vertical (^/v)
        #  - vertical (^/v) then horizontal (</>)
        # as mixing does not seem efficient
        #
        # This means changing direction once and in (at most)
        # 2 possible places:
        #  - (x, prev_y) for the vertical move
        #  - (prev_x, y) for the horizontal move
        # and under the condition that this position is valid
        #
        # Finally, we have multiple combinations:
        #  - A^>A and A>^A
        #  - A^<A and A<^A
        #  - Av>A and A>vA
        #  - Av<A and A<vA
        # and for some reason, the later seem to lead to better
        # results down the line...
        x_buttons = keys_from_delta(dx, (1, 0))
        y_buttons = keys_from_delta(dy, (0, 1))
        options = []
        if dy and (prev_x, y) != invalid_pos:
            options.append(y_buttons + x_buttons)
        if dx and (x, prev_y) != invalid_pos:
            options.append(x_buttons + y_buttons)
        if options:
            seq += options[0 if y_move_first else -1]
        seq += "A"
    return seq


def shortest_num_sequence(code):
    return shortest_sequence(code, num_keypad)


def shortest_dir_sequence(code):
    return shortest_sequence(code, dir_keypad)


# for v in (False, True):
#     y_move_first = v
#     seq1 = "^AvA"
#     seq2 = shortest_dir_sequence(seq1)
#     seq3 = shortest_dir_sequence(seq2)
#     seq4 = shortest_dir_sequence(seq3)
#     print(seq1)
#     print(seq2)
#     print(seq3)
#     print(seq4)


def get_shortest_seq_len(code, nb_robot_direct_keypad):
    seq = shortest_num_sequence(code)
    for n in range(nb_robot_direct_keypad):
        seq = shortest_dir_sequence(seq)
    return len(seq)


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
    # TODO: To be optimised probably by not recomputing the same same over and over:
    # print(get_complexity_sum(codes, 25))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
