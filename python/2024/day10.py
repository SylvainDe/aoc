# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import collections


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_grid_from_lines(string):
    grid = dict()
    for i, l in enumerate(string.splitlines()):
        for j, v in enumerate(l):
            grid[(i, j)] = int(v) if v != "." else -4
    return grid


def get_grid_from_file(file_path=top_dir + "resources/year2024_day10_input.txt"):
    with open(file_path) as f:
        return get_grid_from_lines(f.read())


def get_neighbours(pos):
    x, y = pos
    yield x, y + 1
    yield x, y - 1
    yield x + 1, y
    yield x - 1, y


def get_neighbours_with_val(pos, grid, val):
    for neig in get_neighbours(pos):
        if grid.get(neig, -1) == val:
            yield neig


def get_trailhead_score_sum(grid):
    reachable = set((p, p) for p, v in grid.items() if v == 0)
    for v in range(9):
        assert all(grid[begin] == 0 for begin, _ in reachable)
        assert all(grid[pos] == v for _, pos in reachable)
        new_reachable = set()
        for begin, pos in reachable:
            new_reachable.update(
                (begin, neig) for neig in get_neighbours_with_val(pos, grid, v + 1)
            )
        reachable = new_reachable
        assert all(grid[pos] == v + 1 for _, pos in reachable)
    return len(reachable)


def get_trailhead_score_sum2(grid):
    reachable = {p: 1 for p, v in grid.items() if v == 0}
    for v in range(9):
        assert all(grid[pos] == v for pos in reachable)
        new_reachable = collections.defaultdict(int)
        for pos, nb in reachable.items():
            for neig in get_neighbours_with_val(pos, grid, v + 1):
                new_reachable[neig] += nb
        reachable = new_reachable
        assert all(grid[pos] == v + 1 for pos in reachable)
    return sum(reachable.values())


def run_tests():
    grid = get_grid_from_lines(
        """10..9..
2...8..
3...7..
4567654
...8..3
...9..2
.....01"""
    )
    assert get_trailhead_score_sum(grid) == 3

    grid = get_grid_from_lines(
        """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""
    )
    assert get_trailhead_score_sum(grid) == 36
    assert get_trailhead_score_sum2(grid) == 81


def get_solutions():
    grid = get_grid_from_file()
    print(get_trailhead_score_sum(grid) == 566)
    print(get_trailhead_score_sum2(grid) == 1324)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
