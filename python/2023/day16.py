# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_xxx_from_line(string):
    return string


def get_grid_from_lines(string):
    grid = dict()
    for i, row in enumerate(string.splitlines()):
        for j, val in enumerate(row):
            grid[(i, j)] = val
    return grid


def get_grid_from_file(file_path=top_dir + "resources/year2023_day16_input.txt"):
    with open(file_path) as f:
        return get_grid_from_lines(f.read())

N = (-1, 0)
S = (+1, 0)
W = (0, -1)
E = (0, +1)

next_directions = {
    ".": {
        N: [N],
        E: [E],
        S: [S],
        W: [W],
    },
    "/": {
        N: [E],
        E: [N],
        S: [W],
        W: [S],
    },
    "\\": {
        N: [W],
        W: [N],
        S: [E],
        E: [S],
    },
    "-": {
        N: [W, E],
        S: [W, E],
        E: [E],
        W: [W],
    },
    "|": {
        N: [N],
        S: [S],
        E: [N, S],
        W: [N, S],
    },
}


def get_beam_paths(grid, starting_beam):
    beam_paths = set()
    beam_ends = set([starting_beam])
    while True:
        new_beam_ends = set()
        for val in beam_ends:
            pos, direction = val
            content = grid.get(pos)
            if content is None:
                continue
            if val in beam_paths:
                continue
            beam_paths.add(val)
            i, j = pos
            for dir2 in next_directions[content][direction]:
                di, dj = dir2
                new_beam_ends.add(((i + di, j + dj), dir2))
        if not new_beam_ends:
            return beam_paths
        beam_ends = new_beam_ends

def show_grid(grid):
    xs = [p[0] for p in grid]
    ys = [p[1] for p in grid]
    for i in range(min(xs), max(xs)+1):
        for j in range(min(ys), max(ys)+1):
            pos = (i, j)
            print(grid.get(pos, "#"), end="")
        print()
    print()

def show_paths(paths):
    positions_values = dict()
    for pos, direct in paths:
        positions_values.setdefault(pos, []).append(direct)
    xs = [p[0] for p in positions_values]
    ys = [p[1] for p in positions_values]
    for i in range(min(xs), max(xs)+1):
        for j in range(min(ys), max(ys)+1):
            pos = (i, j)
            directions = positions_values.get(pos, [])
            nb_directions = len(directions)
            if nb_directions == 0:
                value = " "
            elif nb_directions == 1:
                d = directions[0]
                if d == N:
                    value = "N"
                elif d == S:
                    value = "S"
                elif d == W:
                    value = "W"
                elif d == E:
                    value = "E"
                else:
                    1/0
            else:
                value = str(nb_directions)
            print(value, end="")
        print()
    print()

def get_nb_energized_tiles(grid, start=((0, 0), E)):
    return len(set(pos for pos, _ in get_beam_paths(grid, start)))

def get_max_nb_energized_tiles(grid):
    xs = [p[0] for p in grid]
    ys = [p[1] for p in grid]
    min_x, max_x = set([min(xs), max(xs)])
    min_y, max_y = set([min(ys), max(ys)])
    starts = []
    for pos in grid:
        x, y = pos
        if x == min_x:
            starts.append((pos, S))
        if x == max_x:
            starts.append((pos, N))
        if y == min_y:
            starts.append((pos, E))
        if y == max_y:
            starts.append((pos, W))
    return max(get_nb_energized_tiles(grid, s) for s in starts)

def run_tests():
    grid = get_grid_from_lines(
        """.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|...."""
    )
    assert get_nb_energized_tiles(grid) == 46
    assert get_max_nb_energized_tiles(grid) == 51


def get_solutions():
    grid = get_grid_from_file()
    print(get_nb_energized_tiles(grid) == 7477)
    print(get_max_nb_energized_tiles(grid) == 7853)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
