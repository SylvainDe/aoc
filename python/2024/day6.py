# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import itertools

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


directions = {
    "^": (-1, 0),
    "v": (1, 0),
    ">": (0, 1),
    "<": (0, -1),
}


def pairwise_circle(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ... (s<last>,s0)"
    a, b = itertools.tee(iterable)
    first_value = next(b, None)
    return itertools.zip_longest(a, b, fillvalue=first_value)


next_direction = {directions[d1]: directions[d2] for d1, d2 in pairwise_circle("^>v<")}

FREE = 0
WALL = 1


def get_grid_content_from_lines(string):
    guard = None
    grid = dict()
    for i, l in enumerate(string.splitlines()):
        for j, c in enumerate(l):
            pos = (i, j)
            if c == "#":
                grid[pos] = WALL
            else:
                grid[pos] = FREE
                if c in directions:
                    guard = (pos, directions[c])
                else:
                    assert c == "."
    return grid, guard


def get_grid_content_from_file(file_path=top_dir + "resources/year2024_day6_input.txt"):
    with open(file_path) as f:
        return get_grid_content_from_lines(f.read())


def get_next(pos, direc):
    x, y = pos
    dx, dy = direc
    return x + dx, y + dy


def get_path(grid, guard):
    pos, direc = guard
    yield pos, direc
    while True:
        assert grid[pos] == FREE
        next_pos = get_next(pos, direc)
        next_cell = grid.get(next_pos)
        if next_cell is None:
            return
        elif next_cell == FREE:
            pos = next_pos
            yield next_pos, direc
        else:
            assert next_cell == WALL
            direc = next_direction[direc]


def is_looped(grid, guard):
    seen = set()
    for guard in get_path(grid, guard):
        if guard in seen:
            return True
        seen.add(guard)
    return False


def part1(grid, guard):
    return len(set(p for p, _ in get_path(grid, guard)))


def is_looped_with_new_wall(grid, guard, pos):
    assert grid[pos] == FREE
    grid[pos] = WALL
    ret = is_looped(grid, guard)
    grid[pos] = FREE
    return ret


def part2_very_slow(grid, guard):
    return sum(
        is_looped_with_new_wall(grid, guard, pos)
        for pos in grid
        if pos != guard[0] and grid[pos] == FREE
    )


def part2_slow(grid, guard):
    return sum(
        is_looped_with_new_wall(grid, guard, pos)
        for pos in set(p for p, _ in get_path(grid, guard) if p != guard[0])
    )


def part2(grid, guard):
    nb = 0
    seen = set(guard[0])
    path = list(get_path(grid, guard))
    for prev, (pos, _) in zip(path, path[1:]):
        if pos not in seen:
            nb += is_looped_with_new_wall(grid, prev, pos)
            seen.add(pos)
    return nb


def run_tests():
    grid, guard = get_grid_content_from_lines(
        """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""
    )
    assert part1(grid, guard) == 41
    assert not is_looped(grid, guard)
    grid2, guard2 = get_grid_content_from_lines(
        """....#.....
.........#
..........
..#.......
.......#..
..........
.#.#^.....
........#.
#.........
......#..."""
    )
    assert is_looped(grid2, guard2)
    assert part2_very_slow(grid, guard) == 6
    assert part2_slow(grid, guard) == 6
    assert part2(grid, guard) == 6


def get_solutions():
    grid, guard = get_grid_content_from_file()
    print(part1(grid, guard) == 5086)
    print(part2(grid, guard) == 1770)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
