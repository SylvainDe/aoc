# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_info_from_lines(lines, fold_instr="fold along "):
    read_dot = True
    dots = set()
    folds = []
    for l in lines:
        l = l.strip()
        if l == "":
            read_dot = False
        elif read_dot:
            dots.add(tuple([int(v) for v in l.split(",")]))
        elif l.startswith(fold_instr):
            axis, line = l[len(fold_instr) :].split("=")
            folds.append((axis, int(line)))
    return dots, folds


def get_info_from_file(file_path="day13_input.txt"):
    with open(file_path) as f:
        return get_info_from_lines(f)


def show_dots(dots):
    x_vals = {d[0] for d in dots}
    y_vals = {d[1] for d in dots}
    x_range = list(range(min(x_vals), 1 + max(x_vals)))
    y_range = list(range(min(y_vals), 1 + max(y_vals)))
    for y in y_range:
        print("".join("#" if (x, y) in dots else "." for x in x_range))
    print()


def fold_val(val, line):
    assert val != line
    return val if val < line else 2 * line - val


def fold_dot(dot, axis, line):
    return tuple(fold_val(c, line) if i == axis else c for i, c in enumerate(dot))


def fold_dots(dots, axis, line):
    return {fold_dot(d, axis, line) for d in dots}


def apply_folds(dots, folds):
    axis_vals = {"x": 0, "y": 1}
    for axis, line in folds:
        dots = fold_dots(dots, axis_vals[axis], line)
    return dots


def run_tests():
    info = [
        "6,10",
        "0,14",
        "9,10",
        "0,3",
        "10,4",
        "4,11",
        "6,0",
        "6,12",
        "4,1",
        "0,13",
        "10,12",
        "3,4",
        "3,0",
        "8,4",
        "1,10",
        "2,14",
        "8,10",
        "9,0",
        "",
        "fold along y=7",
        "fold along x=5",
    ]
    dots, folds = get_info_from_lines(info)
    assert dots == {
        (9, 10),
        (6, 12),
        (2, 14),
        (9, 0),
        (8, 4),
        (3, 4),
        (10, 4),
        (0, 13),
        (0, 3),
        (8, 10),
        (3, 0),
        (6, 10),
        (10, 12),
        (6, 0),
        (1, 10),
        (4, 11),
        (0, 14),
        (4, 1),
    }
    # Step by step
    dots = fold_dots(dots, 1, 7)
    assert dots == {
        (0, 1),
        (9, 0),
        (6, 2),
        (8, 4),
        (3, 4),
        (4, 3),
        (0, 0),
        (10, 4),
        (0, 3),
        (2, 0),
        (6, 4),
        (1, 4),
        (3, 0),
        (6, 0),
        (4, 1),
        (10, 2),
        (9, 4),
    }
    dots = fold_dots(dots, 0, 5)
    assert dots == {
        (0, 1),
        (4, 4),
        (2, 4),
        (4, 0),
        (0, 4),
        (3, 4),
        (4, 3),
        (0, 0),
        (0, 3),
        (2, 0),
        (4, 2),
        (1, 4),
        (3, 0),
        (0, 2),
        (1, 0),
        (4, 1),
    }
    # All at once
    dots, folds = get_info_from_lines(info)
    dots = apply_folds(dots, folds)
    assert dots == {
        (0, 1),
        (4, 4),
        (2, 4),
        (4, 0),
        (0, 4),
        (3, 4),
        (4, 3),
        (0, 0),
        (0, 3),
        (2, 0),
        (4, 2),
        (1, 4),
        (3, 0),
        (0, 2),
        (1, 0),
        (4, 1),
    }


def get_solutions():
    dots, folds = get_info_from_file()
    print(len(apply_folds(dots, [folds[0]])))
    show_dots(apply_folds(dots, folds))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
