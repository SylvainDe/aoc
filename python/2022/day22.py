# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import itertools

def get_map_from_lines(string):
    map_ = dict()
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
        if c in ('R', 'L'):
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

def get_notes_from_file(file_path="../../resources/year2022_day22_input.txt"):
    with open(file_path) as f:
        return get_notes_from_lines(f.read())

def show_path(map_, path):
    copy = dict()
    for k, v in map_.items():
        copy[k] = "." if v else "#"
    for i, pos in enumerate(path):
        assert map_[pos] == True
        copy[pos] = str(i%10)
    copy[pos] = "*"
    xs = [p[0] for p in copy.keys()]
    ys = [p[1] for p in copy.keys()]
    x_range = list(range(min(xs), max(xs) + 1))
    y_range = list(range(min(ys), max(ys) + 1))
    for x in x_range:
        print("".join(copy.get((x, y), ' ') for y in y_range))

def turn(turn, dx, dy):
    if turn == 'L':
        return (-dy, dx)
    assert turn == 'R'
    return (dy, -dx)

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
    (0, 1):  0,  # Right
    (-1, 0): 3,  # Up
    (0, -1): 2,  # Left
    (1, 0):  1,  # Down
}

def follow_notes(notes, show_debug=False):
    map_, path = notes
    x, y = get_start_pos(map_)
    nb_rows, nb_col = get_map_dim(map_)
    dx, dy = (0, 1)  # Face right
    debugging_path = [(x, y)]
    for ins in path:
        if ins in ('R', 'L'):
            dx, dy = turn(ins, dx, dy)
        else:
            for _ in range(ins):
                for i in itertools.count(1):
                    pos2 = (x+i*dx) % nb_rows, (y+i*dy) % nb_col
                    res = map_.get(pos2)
                    if res is not None:
                        break
                if res:
                    x, y = pos2
                    debugging_path.append(pos2)
                else:
                    break
    if show_debug:
        show_path(map_, debugging_path)
    return 1000 * (x + 1) + 4 * (y + 1) + directions_score[(dx, dy)]

def run_tests():
    notes = get_notes_from_lines("""        ...#
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

10R5L5R10L4R5L5""")
    assert follow_notes(notes) == 6032

def get_solutions():
    notes = get_notes_from_file()
    print(follow_notes(notes) == 66292)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
