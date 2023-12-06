# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import itertools


resource_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../resources/"


def get_map_from_lines(string):
    map_ = {}
    for i, l in enumerate(string.splitlines()):
        for j, c in enumerate(l):
            pos = (i, j)
            if c == ".":
                map_[pos] = True
            elif c == "#":
                map_[pos] = False
            else:
                assert c == " "
    return map_


def get_path(string):
    path = []
    d = 0
    for c in string:
        if c in ("R", "L"):
            if d:
                path.append(d)
                d = 0
            path.append(c)
        else:
            d = d * 10 + int(c)
    if d:
        path.append(d)
    return path


def get_notes_from_lines(string):
    map_, path = string.split("\n\n")
    map_ = get_map_from_lines(map_)
    path = get_path(path.strip())
    return map_, path


def get_notes_from_file(file_path=resource_dir + "year2022_day22_input.txt"):
    with open(file_path) as f:
        return get_notes_from_lines(f.read())


def show_path(map_, path):
    copy = {}
    for k, v in map_.items():
        copy[k] = "." if v else "#"
    for i, pos in enumerate(path):
        assert map_[pos]
        copy[pos] = str(i % 10)
    copy[pos] = "*"
    xs = [p[0] for p in copy]
    ys = [p[1] for p in copy]
    x_range = list(range(min(xs), max(xs) + 1))
    y_range = list(range(min(ys), max(ys) + 1))
    for x in x_range:
        print("".join(copy.get((x, y), " ") for y in y_range) + "    " + str(x))
    print("".join(str(y % 10) for y in y_range))
    print("From", path[0], "to", path[-1])
    print()


def turn(turn, direction):
    # TODO: Use complex numbers ?
    dx, dy = direction
    if turn == "L":
        return (-dy, dx)
    assert turn == "R"
    return (dy, -dx)


def inverse(direction):
    dx, dy = direction
    return -dx, -dy


def get_start_pos(map_):
    x = 0  # Top row
    y = min(j for (i, j), v in map_.items() if i == x and v)
    assert map_[(x, y)] is True
    return x, y


def get_map_dim(map_):
    nb_rows = max(i for i, _ in map_.keys()) + 1
    nb_col = max(j for _, j in map_.keys()) + 1
    return nb_rows, nb_col


directions_score = {
    (0, 1): 0,  # Right
    (-1, 0): 3,  # Up
    (0, -1): 2,  # Left
    (1, 0): 1,  # Down
}


def follow_notes(notes, show_debug=False):
    map_, path = notes
    pos = get_start_pos(map_)
    nb_rows, nb_col = get_map_dim(map_)
    direc = (0, 1)  # Face right
    debugging_path = [pos]
    for ins in path:
        if ins in ("R", "L"):
            direc = turn(ins, direc)
        else:
            for _ in range(ins):
                for i in itertools.count(1):
                    x, y = pos
                    dx, dy = direc
                    pos2 = (x + i * dx) % nb_rows, (y + i * dy) % nb_col
                    res = map_.get(pos2)
                    if res is not None:
                        break
                assert res is not None
                if not res:
                    break
                pos = pos2
                debugging_path.append(pos2)
    if show_debug:
        show_path(map_, debugging_path)
    x, y = pos
    return 1000 * (x + 1) + 4 * (y + 1) + directions_score[direc]


def follow_notes_on_cube(notes, seams, show_debug=False):
    map_, path = notes
    pos = get_start_pos(map_)
    direc = (0, 1)  # Face right
    debugging_path = [pos]
    for ins in path:
        if ins in ("R", "L"):
            direc = turn(ins, direc)
        else:
            for _ in range(ins):
                x, y = pos
                dx, dy = direc
                pos2, direc2 = (x + dx, y + dy), direc
                seams_info = seams.get((pos, direc))
                if seams_info is not None:
                    assert pos2 not in map_
                    pos2, direc2 = seams_info
                res = map_.get(pos2)
                assert res is not None
                if not res:
                    break
                pos = pos2
                direc = direc2
                debugging_path.append(pos)
    if show_debug:
        show_path(map_, debugging_path)
    x, y = pos
    return 1000 * (x + 1) + 4 * (y + 1) + directions_score[direc]


def run_tests():
    notes = get_notes_from_lines(
        """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""
    )
    assert follow_notes(notes) == 6032
    side = 4
    seams = {}
    for i in range(side):
        # Harcode list of seams based on pattern
        #          1111
        #          1111
        #          1111
        #          1111
        #  222233334444
        #  222233334444
        #  222233334444
        #  222233334444
        #          55556666
        #          55556666
        #          55556666
        #          55556666
        # Side 4 to side 6
        pos1, dir1 = (side + i, 3 * side - 1), (0, 1)
        pos2, dir2 = (2 * side, 4 * side - i - 1), (1, 0)
        seams[(pos1, dir1)] = (pos2, dir2)
        # Side 5 to side 2
        pos1, dir1 = (3 * side - 1, 2 * side + i), (1, 0)
        pos2, dir2 = (2 * side - 1, side - i - 1), (-1, 0)
        seams[(pos1, dir1)] = (pos2, dir2)
        # Side 3 to side 1
        pos1, dir1 = (side, side + i), (-1, 0)
        pos2, dir2 = (i, 2 * side), (0, 1)
        seams[(pos1, dir1)] = (pos2, dir2)
        # TODO: add missing seams
    # TODO: Add symetric seam with opposite directions
    assert follow_notes_on_cube(notes, seams) == 5031


def get_solutions():
    notes = get_notes_from_file()
    print(follow_notes(notes) == 66292)
    side = 50
    seams = {}
    for i in range(side):
        # Harcode list of seams based on pattern
        #    111222
        #    111222
        #    111222
        #    333
        #    333
        #    333
        # 444555
        # 444555
        # 444555
        # 666
        # 666
        # 666
        #
        # Side 1 to side 4
        pos1, dir1 = (i, side), (0, -1)
        pos2, dir2 = (3 * side - i - 1, 0), (0, 1)
        seams[(pos1, dir1)] = (pos2, dir2)
        # Side 6 to side 2
        pos1, dir1 = (4 * side - 1, i), (1, 0)
        pos2, dir2 = (0, 2 * side + i), (1, 0)
        seams[(pos1, dir1)] = (pos2, dir2)
        # Side 5 to side 6
        pos1, dir1 = (3 * side - 1, side + i), (1, 0)
        pos2, dir2 = (3 * side + i, side - 1), (0, -1)
        seams[(pos1, dir1)] = (pos2, dir2)
        # Side 4 to side 3
        pos1, dir1 = (2 * side, i), (-1, 0)
        pos2, dir2 = (side + i, side), (0, 1)
        seams[(pos1, dir1)] = (pos2, dir2)
        # Side 1 to side 6
        pos1, dir1 = (0, 50 + i), (-1, 0)
        pos2, dir2 = (3 * side + i, 0), (0, 1)
        seams[(pos1, dir1)] = (pos2, dir2)
        # Side 3 to side 2
        pos1, dir1 = (side + i, 2 * side - 1), (0, 1)
        pos2, dir2 = (side - 1, 2 * side + i), (-1, 0)
        seams[(pos1, dir1)] = (pos2, dir2)
        # Side 2 to side 5
        pos1, dir1 = (i, 3 * side - 1), (0, 1)
        pos2, dir2 = (3 * side - i - 1, 2 * side - 1), (0, -1)
        seams[(pos1, dir1)] = (pos2, dir2)
    # Add symetric seam with opposite directions
    for (pos1, dir1), (pos2, dir2) in dict(seams).items():
        seams[(pos2, inverse(dir2))] = (pos1, inverse(dir1))
    print(follow_notes_on_cube(notes, seams) == 127012)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
