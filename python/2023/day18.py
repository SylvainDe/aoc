# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import itertools

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_instruction_from_line(string):
    direction, nb, color = string.split()
    return direction, int(nb), color


def get_instructions_from_lines(string):
    return [get_instruction_from_line(l) for l in string.splitlines()]


def get_instructions_from_file(file_path=top_dir + "resources/year2023_day18_input.txt"):
    with open(file_path) as f:
        return get_instructions_from_lines(f.read())


directions = {
    'D': (+1, 0),
    'U': (-1, 0),
    'R': (0, +1),
    'L': (0, -1),
}

def get_trench(instructions):
    i, j = 0, 0
    yield i, j
    for d, n, _ in instructions:
        di, dj = directions[d]
        for _ in range(n):
            i += di
            j += dj
            yield i, j

def get_reachable(start, grid):
    print(min(grid), max(grid))
    visited = set()
    to_handle = set([start])
    while to_handle:
        print(len(to_handle), min(to_handle), max(to_handle))
        new_to_handle = set()
        for p in to_handle:
            if p not in visited:
                visited.add(p)
                i, j = p
                for di, dj in directions.values():
                    p2 = i + di, j + dj
                    if p2 in grid and p2 not in visited:
                        new_to_handle.add(p2)
        to_handle = new_to_handle
    return visited

def get_interior_volume(path):
    xs = set(p[0] for p in path)
    ys = set(p[1] for p in path)
    x_range = list(range(min(xs)-1, max(xs)+1+1))
    y_range = list(range(min(ys)-1, max(ys)+1+1))
    empty_spaces = [pos for pos in itertools.product(x_range, y_range) if pos not in path]
    # what are we living for
    abandoned_places = get_reachable((min(x_range), min(y_range)), empty_spaces)
    # I guess we know the score
    return len(x_range) * len(y_range) - len(abandoned_places)

def get_trench_volume(instructions):
    return get_interior_volume(set(get_trench(instructions)))


def run_tests():
    instructions = get_instructions_from_lines(
        """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""
    )
    assert get_trench_volume(instructions) == 62

def get_solutions():
    instructions = get_instructions_from_file()
    print(get_trench_volume(instructions) == 44436)  # SUPER SLOW :(


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
