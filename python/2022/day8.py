# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_trees_from_line(string):
    return [int(c) for c in string]


def get_trees_from_lines(string):
    return [get_trees_from_line(l) for l in string.splitlines()]


def get_trees_from_file(file_path=top_dir + "resources/year2022_day8_input.txt"):
    with open(file_path) as f:
        return get_trees_from_lines(f.read())


def visible_positions(trees):
    visible = set()
    for i, row in enumerate(trees):
        indexed_row = list(enumerate(row))
        for irow in (indexed_row, reversed(indexed_row)):
            maxsofar = -1
            for j, val in irow:
                if val > maxsofar:
                    visible.add((i, j))
                maxsofar = max(val, maxsofar)
    for j in range(len(trees[0])):
        indexed_col = [(i, row[j]) for i, row in enumerate(trees)]
        for icol in (indexed_col, reversed(indexed_col)):
            maxsofar = -1
            for i, val in icol:
                if val > maxsofar:
                    visible.add((i, j))
                maxsofar = max(val, maxsofar)
    return len(visible)


def scenic_score(trees):
    # Naive algo
    scores = []
    for i, row in enumerate(trees):
        for j, val in enumerate(row):
            view_right, view_left, view_top, view_bottom = 0, 0, 0, 0
            before, after = reversed(row[:j]), row[j + 1 :]
            for val2 in after:
                view_right += 1
                if val2 >= val:
                    break
            for val2 in before:
                view_left += 1
                if val2 >= val:
                    break
            before, after = reversed(trees[:i]), trees[i + 1 :]
            for row2 in before:
                view_top += 1
                if row2[j] >= val:
                    break
            for row2 in after:
                view_bottom += 1
                if row2[j] >= val:
                    break
            scores.append(view_right * view_left * view_top * view_bottom)
    return max(scores)


def run_tests():
    trees = get_trees_from_lines(
        """30373
25512
65332
33549
35390"""
    )
    assert visible_positions(trees) == 21
    assert scenic_score(trees) == 8


def get_solutions():
    trees = get_trees_from_file()
    print(visible_positions(trees) == 1816)
    print(scenic_score(trees) == 383520)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
