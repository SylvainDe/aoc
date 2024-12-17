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

WALL = "#"
BOX = "O"
LBOX = "["
RBOX = "]"
BOXES = (BOX, LBOX, RBOX)
ROBOT = "@"


def get_grid_content(strings):
    grid = dict()
    for i, l in enumerate(strings):
        for j, v in enumerate(l):
            pos = (i, j)
            if v == ".":
                continue
            assert v in (WALL, BOX, ROBOT)
            grid[pos] = v
    return grid


def get_instructions(string):
    return [directions[c] for c in string if c in directions]


def get_inputs_from_lines(string):
    sep = "\n\n"
    beg, mid, end = string.partition(sep)
    assert mid == sep
    return get_grid_content(beg.splitlines()), get_instructions(end.strip())


def get_inputs_from_file(file_path=top_dir + "resources/year2024_day15_input.txt"):
    with open(file_path) as f:
        return get_inputs_from_lines(f.read())


def gps(pos):
    x, y = pos
    return 100 * x + y


def find_robot(grid):
    for pos, val in grid.items():
        if val == ROBOT:
            return pos
    return None


def enlarge(grid):
    grid2 = dict()
    for (x, y), val in grid.items():
        if val == WALL:
            a, b = WALL, WALL
        elif val == BOX:
            a, b = LBOX, RBOX
        elif val == ROBOT:
            a, b = ROBOT, None
        else:
            assert False
        grid2[(x, 2 * y)] = a
        if b is not None:
            grid2[(x, 2 * y + 1)] = b
    return grid2


def pos_add(pos, delta, n=1):
    i, j = pos
    di, dj = delta
    return i + n * di, j + n * dj


def display(grid, robot):
    grid = dict(grid)
    grid[robot] = ROBOT
    xs = set(x for x, _ in grid.keys())
    ys = set(y for _, y in grid.keys())
    for x in range(min(xs), max(xs) + 1):
        print("".join(grid.get((x, y), " ") for y in range(min(ys), max(ys) + 1)))


def follow_instructions(grid, instr):
    grid = dict(grid)
    robot = find_robot(grid)
    grid.pop(robot)
    for move in instr:
        do_follow_instructions = True
        boxes_to_move = []
        to_check = set([robot])
        while True:
            to_check = set(p for p in (pos_add(p, move) for p in to_check) if p in grid)
            if not to_check:
                break
            if any(grid[p] == WALL for p in to_check):
                do_follow_instructions = False
                break
            if move[0]:
                for p in set(to_check):
                    c = grid[p]
                    assert c in BOXES
                    if c == LBOX:
                        to_check.add(pos_add(p, (0, 1)))
                    elif c == RBOX:
                        to_check.add(pos_add(p, (0, -1)))
            boxes_to_move.extend(to_check)
        if do_follow_instructions:
            for b in reversed(boxes_to_move):
                dest = pos_add(b, move)
                assert dest not in grid
                grid[dest] = grid.pop(b)
            robot = pos_add(robot, move)
            assert robot not in grid
        # display(grid, robot)
    return sum(gps(p) for p, v in grid.items() if v in (BOX, LBOX))


def run_tests():
    grid, instr = get_inputs_from_lines(
        """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########


<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""
    )
    assert follow_instructions(grid, instr) == 10092
    assert follow_instructions(enlarge(grid), instr) == 9021
    grid, instr = get_inputs_from_lines(
        """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""
    )
    assert follow_instructions(grid, instr) == 2028


def get_solutions():
    grid, instr = get_inputs_from_file()
    print(follow_instructions(grid, instr) == 1559280)
    print(follow_instructions(enlarge(grid), instr) == 1576353)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
