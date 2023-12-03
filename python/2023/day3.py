# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime

def get_grid_from_file(file_path="../../resources/year2023_day3_input.txt"):
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


def get_adjacent_symbols(row, beg, end, grid):
    symbols = []
    for i in range(row-1, row + 1 + 1):
        for j in range(beg-1, end + 1):
            if i >= 0 and j >= 0:
                try:
                     c = grid[i][j]
                except IndexError:
                     continue
                if not c.isdigit() and c != ".":
                    # print(row, beg, end, grid[row][beg:end], c, i, j, "YYY")
                    symbols.append((i, j, c))
    # print(row, beg, end, grid[row][beg:end], "N")
    return symbols

def get_parts(grid):
    parts = []
    current_nb, nb_len = 0, 0
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
             if c.isdigit():
                 current_nb = 10 * current_nb + int(c)
                 nb_len += 1
             elif current_nb:
                 parts.append((current_nb, get_adjacent_symbols(i, j - nb_len, j, grid)))
                 current_nb, nb_len = 0, 0
        if current_nb:
            parts.append((current_nb, get_adjacent_symbols(i, j - nb_len, j, grid)))
            current_nb, nb_len = 0, 0
    return parts

def get_part_numbers(grid):
    return sum(p for p, s in get_parts(grid) if s)

def get_gears(grid):
    gears_candidate = dict()
    for p, symbols in get_parts(grid):
        for (i, j, c) in symbols:
            if c == "*":
                gears_candidate.setdefault((i, j), []).append(p)
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
