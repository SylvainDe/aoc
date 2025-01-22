# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"

#   0
# 0 +-------> x
#   |
#   |
#   v
#   y

carts_dir = {
    ">": ("-", (1, 0)),
    "<": ("-", (-1, 0)),
    "^": ("|", (0, -1)),
    "v": ("|", (0, 1)),
}

LEFT, STRAIGHT, RIGHT = 0, 1, 2

track_turns = {
    "/": [("<>", LEFT), ("^v", RIGHT)],
    "\\": [("<>", RIGHT), ("^v", LEFT)],
    "|": [("^v", STRAIGHT)],
    "-": [("<>", STRAIGHT)],
}


def compute_track_turns(track_turns):
    ret = dict()
    for t, lst in track_turns.items():
        for s, direct in lst:
            for c in s:
                ret[(t, carts_dir[c][1])] = direct
    return ret


track_turns = compute_track_turns(track_turns)


track_types = set("-|/\\+")


def get_track_from_lines(string):
    track = dict()
    carts = dict()
    for y, l in enumerate(string.splitlines()):
        for x, v in enumerate(l):
            pos = x, y
            cart = carts_dir.get(v, None)
            if cart is not None:
                v, direct = cart
                carts[pos] = (direct, LEFT)
            if v in track_types:
                track[pos] = v
    return track, carts


def get_track_from_file(file_path=top_dir + "resources/year2018_day13_input.txt"):
    with open(file_path) as f:
        return get_track_from_lines(f.read())


def show_track(track, carts):
    track = dict(track)
    for pos in carts.keys():
        track[pos] = "X"
    ys = set(y for x, y in track)
    xs = set(x for x, y in track)
    x_range = range(min(xs), max(xs) + 1)
    y_range = range(min(ys), max(ys) + 1)
    print(" " + "".join(str(x % 10) for x in x_range))
    for y in y_range:
        print(str(y % 10) + "".join(track.get((x, y), " ") for x in x_range))
    # input()


def do_turn(direction, turn):
    dx, dy = direction
    if turn == LEFT:
        return dy, -dx
    elif turn == RIGHT:
        return -dy, dx
    else:
        assert turn == STRAIGHT
        return direction


def find_crashes(track, carts):
    carts = dict(carts)
    crashes = []
    while True:
        if len(carts) <= 1:
            break
        for pos in sorted(carts.keys()):
            if pos not in carts:
                continue
            direct, next_turn = carts.pop(pos)
            x, y = pos
            dx, dy = direct
            pos = x + dx, y + dy
            if pos in carts:
                carts.pop(pos)
                crashes.append(pos)
                continue
            t = track[pos]
            if t == "+":
                direct = do_turn(direct, next_turn)
                next_turn = (next_turn + 1) % 3
            else:
                direct = do_turn(direct, track_turns[(t, direct)])
            carts[pos] = direct, next_turn
    return crashes, list(carts.keys())


def run_tests():
    track, carts = get_track_from_lines(
        """/->-\\
|   |  /----\\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/
"""
    )
    assert find_crashes(track, carts)[0][0] == (7, 3)
    track, carts = get_track_from_lines(
        """/>-<\\
|   |
| /<+-\\
| | | v
\>+</ |
  |   ^
  \<->/"""
    )
    assert find_crashes(track, carts)[1] == [(6, 4)]


def get_solutions():
    track, carts = get_track_from_file()
    crashes, remaining = find_crashes(track, carts)
    print(crashes[0] == (8, 3))
    print(remaining == [(73, 121)])


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
