# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_area(file_path=top_dir + "resources/year2020_day3_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]


def get_number_of_trees(area, dx=3, dy=1):
    x = 0
    path = []
    for line in area[::dy]:
        path.append(line[x])
        x = (x + dx) % len(line)
    return sum(x == "#" for x in path)


def get_number_of_tree_for_slopes(area, slopes):
    prod = 1
    for dx, dy in slopes:
        prod *= get_number_of_trees(area, dx, dy)
    return prod


slopes = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2),
]


def run_tests():
    area = [
        "..##.......",
        "#...#...#..",
        ".#....#..#.",
        "..#.#...#.#",
        ".#...##..#.",
        "..#.##.....",
        ".#.#.#....#",
        ".#........#",
        "#.##...#...",
        "#...##....#",
        ".#..#...#.#",
    ]
    assert get_number_of_trees(area) == 7
    assert get_number_of_trees(area, 1, 1) == 2
    assert get_number_of_trees(area, 3, 1) == 7
    assert get_number_of_trees(area, 5, 1) == 3
    assert get_number_of_trees(area, 7, 1) == 4
    assert get_number_of_trees(area, 1, 2) == 2
    assert get_number_of_tree_for_slopes(area, slopes) == 336


def get_solutions():
    area = get_area()
    print(get_number_of_trees(area) == 178)
    print(get_number_of_tree_for_slopes(area, slopes) == 3492520200)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
