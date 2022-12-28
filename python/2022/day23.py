# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import collections
import itertools


def get_elves_from_lines(string):
    elves = set()
    for x, l in enumerate(string.splitlines()):
        for y, c in enumerate(l):
            assert c in (".", "#")
            if c == "#":
                elves.add((x, y))
    return elves


def get_elves_from_file(file_path="../../resources/year2022_day23_input.txt"):
    with open(file_path) as f:
        return get_elves_from_lines(f.read())


r = (0, -1, 1)  # "0" must be first

attempts_original = [
    # N
    tuple((-1, c) for c in r),
    # S
    tuple((1, c) for c in r),
    # W
    tuple((c, -1) for c in r),
    # E
    tuple((c, 1) for c in r),
]

neighbours = tuple(t for t in itertools.product(r, repeat=2) if t != (0, 0))


def show_set(s):
    xs = [p[0] for p in s]
    ys = [p[1] for p in s]
    x_range = list(range(min(xs), max(xs) + 1))
    y_range = list(range(min(ys), max(ys) + 1))
    for x in x_range:
        print("".join(("#" if (x, y) in s else " ") for y in y_range) + "    " + str(x))
    print("".join(str(y % 10) for y in y_range))
    print()


def play_rounds(elves, nb_round):
    attempts = collections.deque(attempts_original)
    for i in itertools.count(start=1) if nb_round is None else range(1, nb_round + 1):
        proposals = {}
        elves2 = set()
        for pos in elves:
            x, y = pos
            if not any((x + dx, y + dy) in elves for dx, dy in neighbours):
                elves2.add(pos)
            else:
                for a in attempts:
                    candidates = [(x + dx, y + dy) for dx, dy in a]
                    if not any(c in elves for c in candidates):
                        proposals.setdefault(candidates[0], []).append(pos)
                        break
                else:
                    elves2.add(pos)
        move = False
        for pos, lst in proposals.items():
            if len(lst) > 1:
                for e in lst:
                    assert e not in elves2
                    elves2.add(e)
            else:
                assert pos not in elves2
                elves2.add(pos)
                move = True
        if nb_round is None and not move:
            return i
        attempts.rotate(-1)
        assert len(elves) == len(elves2)
        elves = elves2
    assert nb_round is not None
    xs = [p[0] for p in elves]
    ys = [p[1] for p in elves]
    return (1 + max(xs) - min(xs)) * (1 + max(ys) - min(ys)) - len(elves)


def run_tests():
    elves = get_elves_from_lines(
        """.....
..##.
..#..
.....
..##.
....."""
    )
    play_rounds(elves, 3)
    elves = get_elves_from_lines(
        """..............
..............
.......#......
.....###.#....
...#...#.#....
....#...##....
...#.###......
...##.#.##....
....#..#......
..............
..............
.............."""
    )
    assert play_rounds(elves, 10) == 110
    assert play_rounds(elves, None) == 20

    elves = get_elves_from_lines(
        """.......#......
....#......#..
..#.....#.....
......#.......
...#....#.#..#
#.............
....#.....#...
..#.....#.....
....#.#....#..
.........#....
....#......#..
.......#......"""
    )
    assert play_rounds(elves, None) == 1


def get_solutions():
    elves = get_elves_from_file()
    print(play_rounds(elves, 10) == 4218)
    print(play_rounds(elves, None) == 976)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
