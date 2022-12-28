# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import itertools

blizzards_directions = {
    "^": (-1, 0),
    "v": (1, 0),
    ">": (0, 1),
    "<": (0, -1),
}


def get_map_info_from_lines(string):
    walls = set()
    blizzards = []
    for i, l in enumerate(string.splitlines()):
        for j, c in enumerate(l):
            pos = i, j
            if c == "#":
                walls.add(pos)
            elif c in blizzards_directions:
                blizzards.append((pos, blizzards_directions[c]))
            else:
                assert c == "."
    return walls, blizzards


def get_map_info_from_file(file_path="../../resources/year2022_day24_input.txt"):
    with open(file_path) as f:
        return get_map_info_from_lines(f.read())


def show_grid(walls, blizzards, positions):
    grid = {}
    for w in walls:
        assert w not in grid
        grid[w] = "#"
    for b in blizzards:
        assert b not in grid
        grid[b] = "B"
    for p in positions:
        assert p not in grid
        grid[p] = "p"
    print(grid)
    xs = [p[0] for p in grid]
    ys = [p[1] for p in grid]
    x_range = list(range(min(xs), max(xs) + 1))
    y_range = list(range(min(ys), max(ys) + 1))
    for x in x_range:
        print("".join(grid.get((x, y), " ") for y in y_range) + "    " + str(x))
    print("".join(str(y % 10) for y in y_range))
    print()


def possible_moves(pos):
    x, y = pos
    yield x + 0, y + 0
    yield x + 1, y + 0
    yield x - 1, y + 0
    yield x + 0, y + 1
    yield x + 0, y - 1


def get_begin_and_end(walls):
    by_lines = {}
    for (i, j) in walls:
        by_lines.setdefault(i, []).append(j)
    lines = by_lines.keys()
    for f in (min, max):
        x = f(lines)
        row = set(by_lines[x])
        val = next(iter(set(range(min(row), max(row) + 1)) - row))
        yield x, val


def get_grid_dim(walls):
    nb_rows = max(i for i, _ in walls) + 1
    nb_col = max(j for _, j in walls) + 1
    return nb_rows, nb_col


def get_blizzard_position(blizzard, dim, time):
    (x, y), (dx, dy) = blizzard
    nb_rows, nb_col = dim
    return (
        (x + time * dx - 1) % (nb_rows - 2) + 1,
        (y + time * dy - 1) % (nb_col - 2) + 1,
    )


def part1(map_info):
    walls, blizzards = map_info
    walls = set(walls)
    begin, end = get_begin_and_end(walls)
    (nb_rows, nb_col) = get_grid_dim(walls)
    # Block entrance and exit
    for y in range(nb_col):
        walls.add((-1, y))
        walls.add((nb_rows, y))
    positions = [begin]
    for t in itertools.count():
        bs = set(get_blizzard_position(b, (nb_rows, nb_col), t) for b in blizzards)
        obs = walls | bs
        positions2 = set()
        for p in positions:
            for pos2 in possible_moves(p):
                if pos2 not in obs:
                    positions2.add(pos2)
        positions = positions2
        if end in positions:
            return t
    return None


def part2(map_info):
    walls, blizzards = map_info
    walls = set(walls)
    begin, end = get_begin_and_end(walls)
    (nb_rows, nb_col) = get_grid_dim(walls)
    positions = [(begin, False, False)]
    # Block entrance and exit
    for y in range(nb_col):
        walls.add((-1, y))
        walls.add((nb_rows, y))
    for t in itertools.count():
        bs = set(get_blizzard_position(b, (nb_rows, nb_col), t) for b in blizzards)
        obs = walls | bs
        positions2 = set()
        for (p, end_reached, beg_reached) in positions:
            end_reached2 = end_reached or p == end
            beg_reached2 = beg_reached or (end_reached2 and p == begin)
            for pos2 in possible_moves(p):
                if pos2 not in obs:
                    positions2.add((pos2, end_reached2, beg_reached2))
        positions = positions2
        if (end, True, True) in positions:
            return t
    return None


def run_tests():
    map_info = get_map_info_from_lines(
        """#.#####
#.....#
#>....#
#.....#
#...v.#
#.....#
#####.#"""
    )
    assert part1(map_info) == 9  # I suspect an off-by-one error...
    map_info = get_map_info_from_lines(
        """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#"""
    )
    assert part1(map_info) == 18
    assert part2(map_info) == 54


def get_solutions():
    map_info = get_map_info_from_file()
    print(part1(map_info) == 373)
    print(part2(map_info) == 997)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
