# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import itertools

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_rolls_from_lines(string):
    return {
        (i, j)
        for i, l in enumerate(string.splitlines())
        for j, c in enumerate(l)
        if c == "@"
    }


def get_rolls_from_file(file_path=top_dir + "resources/year2025_day4_input.txt"):
    with open(file_path) as f:
        return get_rolls_from_lines(f.read())


def neighbours(point):
    x, y = point
    for dx, dy in itertools.product([-1, 0, 1], repeat=2):
        if (dx, dy) != (0, 0):
            yield x + dx, y + dy


def is_available(roll, rolls):
    return sum(r2 in rolls for r2 in neighbours(roll)) < 4


def get_available_rolls(rolls):
    return (r for r in rolls if is_available(r, rolls))


def get_nb_available_rolls(rolls):
    return sum(1 for r in get_available_rolls(rolls))


def get_available_rolls_with_removal(rolls):
    available = set()
    while True:
        to_remove = set(get_available_rolls(rolls))
        if not to_remove:
            return available
        rolls = rolls - to_remove
        available |= to_remove


def run_tests():
    rolls = get_rolls_from_lines(
        """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""
    )
    assert get_nb_available_rolls(rolls) == 13
    assert len(get_available_rolls_with_removal(rolls)) == 43


def get_solutions():
    rolls = get_rolls_from_file()
    print(get_nb_available_rolls(rolls) == 1523)
    print(len(get_available_rolls_with_removal(rolls)) == 9290)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
