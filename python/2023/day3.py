# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import itertools


resource_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../resources/"

def get_grid_from_file(file_path=resource_dir + "year2023_day3_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]



def run_tests():
    grid = [
"467..114..",
"...*......",
"..35..633.",
"......#...",
"617*......",
".....+.58.",
"..592.....",
"......755.",
"...$.*....",
".664.598..",
    ]
    assert get_part_numbers(grid) == 4361
    assert get_gears(grid) == 467835
    grid = [
"467..114..",
"..........",
"......*123",
    ]
    assert get_part_numbers(grid) == 123


def get_data_from_grid(grid):
    symbols = dict()
    numbers = []
    current_nb, nb_len = 0, 0
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c.isdigit():
                current_nb = 10 * current_nb + int(c)
                nb_len += 1
            else:
                if current_nb:
                    numbers.append((i, j - nb_len, j, current_nb))
                    current_nb, nb_len = 0, 0
                if c != ".":
                    symbols[(i, j)] = c
        if current_nb:
            j = len(row)
            numbers.append((i, j - nb_len, j, current_nb))
            current_nb, nb_len = 0, 0
    # for row, beg, end, n in numbers:
    #     assert 0 <= beg < end
    #     assert str(n) == grid[row][beg:end]
    return symbols, numbers


def get_adjacent_symbols(row, beg, end, symbols):
    return [(pos, symbols[pos])
            for pos in itertools.product(range(row - 1, row + 1 + 1), range(beg - 1 , end + 1))
            if pos in symbols]


def get_parts(grid):
    symbols, numbers = get_data_from_grid(grid)
    return [(n, get_adjacent_symbols(row, beg, end, symbols))
            for row, beg, end, n in numbers]


def get_part_numbers(grid):
    return sum(p for p, s in get_parts(grid) if s)


def get_gears(grid):
    gears_candidate = dict()
    for p, symbols in get_parts(grid):
        for (pos, c) in symbols:
            if c == "*":
                gears_candidate.setdefault(pos, []).append(p)
    return sum(l[0] * l[1] for pos, l in gears_candidate.items() if len(l) == 2)


def get_solutions():
    grid = get_grid_from_file()
    print(get_part_numbers(grid) == 526404)
    print(get_gears(grid) == 84399773)

if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
