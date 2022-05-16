# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import collections
import itertools


def get_sea_from_file(file_path="day25_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]


GridInfo = collections.namedtuple(
    "GridInfo", ["height", "width", "east_facing", "south_facing"]
)


def get_info_from_sea_grid(sea_grid):
    east_facing = set()  # ">"
    south_facing = set()  # "v"
    height = len(sea_grid)
    width = len(sea_grid[0])
    for i, line in enumerate(sea_grid):
        assert len(line) == width
        for j, val in enumerate(line):
            p = (i, j)
            if val == "v":
                south_facing.add(p)
            elif val == ">":
                east_facing.add(p)
            else:
                assert val == "."
    return GridInfo(height, width, east_facing, south_facing)


def show_sea(grid_info):
    cucumber = (
        lambda p: ">"
        if p in grid_info.east_facing
        else "v"
        if p in grid_info.south_facing
        else "."
    )
    for i in range(grid_info.height):
        print("".join(cucumber((i, j)) for j in range(grid_info.width)))
    print()


def next_step(grid_info):
    # Move East-facing herd
    adjacent = [
        ((i, j), (i, (j + 1) % grid_info.width)) for i, j in grid_info.east_facing
    ]
    east2 = set(
        p1 if (p2 in grid_info.east_facing or p2 in grid_info.south_facing) else p2
        for p1, p2 in adjacent
    )
    # Move South-facing herd
    adjacent = [
        ((i, j), ((i + 1) % grid_info.height, j)) for i, j in grid_info.south_facing
    ]
    south2 = set(
        p1 if (p2 in east2 or p2 in grid_info.south_facing) else p2
        for p1, p2 in adjacent
    )
    return GridInfo(grid_info.height, grid_info.width, east2, south2)


def next_steps(info):
    for i in itertools.count(start=1):
        info2 = next_step(info)
        if info == info2:
            return i
        info = info2


def run_tests():
    sea = [
        "...>...",
        ".......",
        "......>",
        "v.....>",
        "......>",
        ".......",
        "..vvv..",
    ]
    info = get_info_from_sea_grid(sea)
    info = next_step(info)

    sea = [
        "v...>>.vv>",
        ".vv>>.vv..",
        ">>.>v>...v",
        ">>v>>.>.v.",
        "v>v.vv.v..",
        ">.>>..v...",
        ".vv..>.>v.",
        "v.v..>>v.v",
        "....v..v.>",
    ]
    info = get_info_from_sea_grid(sea)
    info = next_step(info)

    info = get_info_from_sea_grid(sea)
    assert next_steps(info) == 58


def get_solutions():
    sea = get_sea_from_file()
    info = get_info_from_sea_grid(sea)
    print(next_steps(info))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
