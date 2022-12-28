# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime

DIRECTIONS = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, 1),
    "D": (0, -1),
}


def get_directions_from_line(string):
    left, mid, right = string.partition(" ")
    assert mid == " "
    assert left in DIRECTIONS
    return (DIRECTIONS[left], int(right))


def get_directions_from_lines(string):
    return [get_directions_from_line(l) for l in string.splitlines()]


def get_directions_from_file(file_path="../../resources/year2022_day9_input.txt"):
    with open(file_path) as f:
        return get_directions_from_lines(f.read())


def sign(x):
    if x < 0:
        return -1
    if x > 0:
        return 1
    return 0


def add_tuple(t1, t2):
    return tuple(i + j for i, j in zip(t1, t2))


def follow(head, tail):
    hx, hy = head
    tx, ty = tail
    t_pos = {tail}
    while abs(hx - tx) > 1 or abs(hy - ty) > 1:
        tx += sign(hx - tx)
        ty += sign(hy - ty)
        t_pos.add((tx, ty))
    return (tx, ty), t_pos


def part1(directions):
    head_tuple = (0, 0)
    tail_tuple = head_tuple
    t_seen = {tail_tuple}
    for tuple_dir, step in directions:
        for _ in range(step):
            head_tuple = add_tuple(head_tuple, tuple_dir)
            tail_tuple, new_pos = follow(head_tuple, tail_tuple)
            t_seen.update(new_pos)
    return len(t_seen)


def part2(directions):
    rope = [(0, 0) for _ in range(10)]
    t_seen = set()
    for tuple_dir, step in directions:
        for _ in range(step):
            rope[0] = add_tuple(rope[0], tuple_dir)
            for i in range(1, len(rope)):
                rope[i], new_pos = follow(rope[i - 1], rope[i])
                if i == len(rope) - 1:
                    t_seen.update(new_pos)
    return len(t_seen)


def run_tests():
    directions = get_directions_from_lines(
        """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""
    )
    assert part1(directions) == 13
    assert part2(directions) == 1
    directions = get_directions_from_lines(
        """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""
    )
    assert part2(directions) == 36


def get_solutions():
    directions = get_directions_from_file()
    print(part1(directions) == 6337)
    print(part2(directions) == 2455)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
