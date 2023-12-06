# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import itertools
import collections


resource_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../resources/"

RUN_LONG_TESTS = False


def string_to_seat_layout(string):
    return {
        (i, j): s
        for i, line in enumerate(string.splitlines())
        for j, s in enumerate(line)
    }


def seat_layout_to_string(seats):
    m = max(i for i, j in seats.keys())
    n = max(j for i, j in seats.keys())
    return "\n".join("".join(seats[(i, j)] for j in range(n + 1)) for i in range(m + 1))


def get_seat_layout_from_file(file_path=resource_dir + "year2020_day11_input.txt"):
    with open(file_path) as f:
        return string_to_seat_layout(f.read())


directions = [pos for pos in itertools.product((-1, 0, +1), repeat=2) if pos != (0, 0)]


def get_new_seat_value_1(seat, nb_neigh):
    if seat == "L":
        return "#" if nb_neigh == 0 else seat
    if seat == "#":
        return "L" if nb_neigh >= 4 else seat
    return seat


def get_new_seats1(seats):
    neighbours_count = collections.Counter(
        (x + dx, y + dy)
        for (x, y), seat in seats.items()
        if seat == "#"
        for dx, dy in directions
    )
    return {
        pos: get_new_seat_value_1(seat, neighbours_count[pos])
        for pos, seat in seats.items()
    }


def get_new_seat_value_rule2(seat, nb_visible):
    if seat == "L":
        return "#" if nb_visible == 0 else seat
    if seat == "#":
        return "L" if nb_visible >= 5 else seat
    return seat


def get_new_seats2(seats):
    visible_count = collections.Counter()
    for (x, y), seat in seats.items():
        if seat == "#":
            for dx, dy in directions:
                for d in itertools.count(start=1):
                    pos = x + (d * dx), y + (d * dy)
                    seat = seats.get(pos, None)
                    if seat != ".":
                        visible_count[pos] += 1
                        break
    return {
        pos: get_new_seat_value_rule2(seat, visible_count[pos])
        for pos, seat in seats.items()
    }


def get_nb_seat_on_fixedpoint(seats, func):
    while True:
        new_seats = func(seats)
        if new_seats == seats:
            break
        seats = new_seats
    return sum(seat == "#" for seat in seats.values())


def run_tests():
    example1 = string_to_seat_layout(
        """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""
    )
    example2 = string_to_seat_layout(
        """#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##"""
    )
    example3a = string_to_seat_layout(
        """#.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##"""
    )
    example3b = string_to_seat_layout(
        """#.LL.LL.L#
#LLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLLL.L
#.LLLLL.L#"""
    )

    assert example2 == get_new_seats1(example1)
    assert example3a == get_new_seats1(example2)
    assert get_nb_seat_on_fixedpoint(example1, get_new_seats1) == 37

    assert example2 == get_new_seats2(example1)
    assert example3b == get_new_seats2(example2)
    assert get_nb_seat_on_fixedpoint(example1, get_new_seats2) == 26


def get_solutions():
    seat_layout = get_seat_layout_from_file()
    print(get_nb_seat_on_fixedpoint(seat_layout, get_new_seats1) == 2204)
    if RUN_LONG_TESTS:
        print(get_nb_seat_on_fixedpoint(seat_layout, get_new_seats2) == 1986)


if __name__ == "__main__":
    RUN_LONG_TESTS = True
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
