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

WALL = '#'
BOX = 'O'

def get_grid_content(strings):
    grid = dict()
    robot = None
    for i, l in enumerate(strings):
        for j, v in enumerate(l):
            pos = (i, j)
            if v == '.':
                continue
            elif v == '@':
                assert robot is None
                robot = pos
                continue
            assert v in (WALL, BOX)
            grid[pos] = v
    return grid, robot

def get_instructions(string):
    return [directions[c] for c in string if c in directions]

def get_inputs_from_lines(string):
    sep = '\n\n'
    beg, mid, end = string.partition(sep)
    assert mid == sep
    grid, robot = get_grid_content(beg.splitlines())
    return grid, robot, get_instructions(end.strip())


def get_inputs_from_file(file_path=top_dir + "resources/year2024_day15_input.txt"):
    with open(file_path) as f:
        return get_inputs_from_lines(f.read())

def gps(pos):
    x, y = pos
    ret = 100 * x + y
    # print(pos, ret)
    return ret

def follow_instructions(grid, robot, instr):
    i, j = robot
    for di, dj in instr:
        do_follow_instructions = True
        boxes = []
        for step in itertools.count(start=1):
            pos = i + step * di, j + step * dj
            content = grid.get(pos, None)
            if content is None:
                break
            elif content == WALL:
                do_follow_instructions = False
            else:
                assert content == BOX
                boxes.append(pos)
        if do_follow_instructions:
            free_pos = i + step * di, j + step * dj
            assert free_pos not in grid
            i, j = i + di, j + dj
            if (i, j) in grid:
                grid[free_pos] = grid[(i, j)]
                grid.pop((i, j))
    # for x in range(0, 1 + max(x for x, y in grid)):
    #     print("".join(grid.get((x, y), " ") for y in range(0, 1 + max(y for x, y in grid))))
    # print()
    ret = sum(gps(p) for p, v in grid.items() if v == BOX)
    # print(ret)
    return ret 
        

def run_tests():
    grid, robot, instr = get_inputs_from_lines(
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
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^""")
    assert follow_instructions(grid, robot, instr) == 10092
    grid, robot, instr = get_inputs_from_lines("""########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<""")
    assert follow_instructions(grid, robot, instr) == 2028


def get_solutions():
    grid, robot, instr = get_inputs_from_file()
    print(follow_instructions(grid, robot, instr))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
