# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_trees_from_line(string):
    return [int(c) for c in string]

def get_trees_from_lines(string):
    return [get_trees_from_line(l) for l in string.splitlines()]

def get_trees_from_file(file_path="../../resources/year2022_day8_input.txt"):
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
                    visible.add((i,j))
                maxsofar = max(val, maxsofar)
    for j in range(len(trees[0])):
        indexed_col = [(i, row[j]) for i, row in enumerate(trees)]
        for icol in (indexed_col, reversed(indexed_col)):
            maxsofar = -1
            for i, val in icol:
                if val > maxsofar:
                    visible.add((i,j))
                maxsofar = max(val, maxsofar)
#    for i, row in enumerate(trees):
#        print("".join((str(val) if (i,j) in visible else " ") for j, val in enumerate(row)))
    return len(visible)

def run_tests():
    trees = get_trees_from_lines("""30373
25512
65332
33549
35390""")
    print(visible_positions(trees))

def get_solutions():
    trees = get_trees_from_file()
    print(visible_positions(trees))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
