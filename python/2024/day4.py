# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import itertools


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_grid_from_lines(string):
    return [l for l in string.splitlines()]


def get_grid_from_file(file_path=top_dir + "resources/year2024_day4_input.txt"):
    with open(file_path) as f:
        return get_grid_from_lines(f.read())


directions = [pos for pos in itertools.product((-1, 0, +1), repeat=2) if pos != (0, 0)]
directions_diag = [pos for pos in itertools.product((-1, +1), repeat=2)]

def is_word(word, pos, direction, grid_dict, start=0):
    x, y = pos
    dx, dy = direction
    return all(
        grid_dict.get((x+(i-start)*dx, y+(i-start)*dy)) == c
        for i, c in enumerate(word)
    )


def get_number(word, grid):
    grid_dict = {(i, j): c for i, line in enumerate(grid) for j, c in enumerate(line)}
    nb = 0
    for pos, c in grid_dict.items():
        if c == word[0]:
            for d in directions:
                if is_word(word, pos, d, grid_dict):
                    nb += 1
    return nb


def get_number2(word, grid):
    grid_dict = {(i, j): c for i, line in enumerate(grid) for j, c in enumerate(line)}
    nb = 0
    crossing_pos = 1
    for pos, c in grid_dict.items():
        if c == word[crossing_pos]:
            if sum(is_word(word, pos, d, grid_dict, crossing_pos) for d in directions_diag) == 2:
                nb+=1
    return nb


def run_tests():
    grid = get_grid_from_lines(
        """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""
    )
    assert get_number("XMAS", grid) == 18
    assert get_number2("MAS", grid) == 9


def get_solutions():
    grid = get_grid_from_file()
    print(get_number("XMAS", grid) == 2551)
    print(get_number2("MAS", grid) == 1985)

if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
