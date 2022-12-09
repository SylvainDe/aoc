# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime

DIRECTIONS = {
    'R': (1, 0),
    'L': (-1, 0),
    'U': (0, 1),
    'D': (0, -1),
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


def part1(directions):
    hx, hy, tx, ty = [0] * 4
    t_seen = { (tx, ty) }
    for (tdx, tdy), step in directions:
        for _ in range(step):
            hx += tdx
            hy += tdy
            while abs(hx - tx) > 1 or abs(hy - ty) > 1:
                tx += sign(hx-tx)
                ty += sign(hy-ty)
                t_seen.add((tx, ty))
    return len(t_seen)


def part2(directions):
    rope = [(0, 0) for _ in range(10)]
    t_seen = { (0, 0) }
    for (tdx, tdy), step in directions:
        for _ in range(step):
            hx, hy = rope[0]
            hx += tdx
            hy += tdy
            rope[0] = hx, hy
            for i in range(1, len(rope)):
                is_last = i == len(rope) - 1
                hx, hy = rope[i-1]
                tx, ty = rope[i]
                while abs(hx - tx) > 1 or abs(hy - ty) > 1:
                    tx += sign(hx-tx)
                    ty += sign(hy-ty)
                    if is_last:
                        t_seen.add((tx, ty))
                rope[i] = tx, ty
    return len(t_seen)


def run_tests():
    directions = get_directions_from_lines("""R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2""")
    assert part1(directions) == 13
    assert part2(directions) == 1
    directions = get_directions_from_lines("""R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20""")
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
