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

def turn(turn, dx, dy):
    if turn == 'L':
        return (-dy, dx)
    assert turn == 'R'
    return (dy, -dx)

directions_score = {
    (0, 1):  0,  # Right
    (-1, 0): 3,  # Up
    (0, -1): 2,  # Left
    (1, 0):  1,  # Down
}

def follow_notes(notes):
    map_, path = notes
    x = 0  # Top row
    y = min(j for (i, j), v in map_.items() if i == x and v)
    nb_rows = max(i for i, _ in map_.keys()) + 1
    nb_col = max(j for _, j in map_.keys()) + 1
    assert map_[(x, y)] is True
    dx, dy = (0, 1)  # Face right
    for ins in path:
        if ins in ('R', 'L'):
            dx, dy = turn(ins, dx, dy)
        else:
            for _ in range(ins):
                x2, y2 = x+dx, y+dy
                res = map_.get((x2, y2))
                if res is None:
                    for i in itertools.count(1):
                        x2, y2 = (x+i*dx) % nb_rows, (y+i*dy) % nb_col
                        res = map_.get((x2, y2))
                        if res is not None:
                            break
                if res:
                    x, y = x2, y2
                else:
                    break
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
