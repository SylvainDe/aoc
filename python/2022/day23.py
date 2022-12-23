# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import collections
import itertools

def get_elves_from_lines(string):
    elves = set()
    for x, l in enumerate(string.splitlines()):
        for y, c in enumerate(l):
            assert c in ('.', '#')
            if c == '#':
                elves.add((x, y))
    return elves

def get_elves_from_file(file_path="../../resources/year2022_day23_input.txt"):
    with open(file_path) as f:
        return get_elves_from_lines(f.read())


attempts_original = [
    # N
    tuple((-1, c) for c in (0, -1, 1)),
    # S
    tuple((1, c) for c in (0, -1, 1)),
    # W
    tuple((c, -1) for c in (0, -1, 1)),
    # E
    tuple((c, 1) for c in (0, -1, 1)),
]

def neighbours(pos):
    x, y = pos
    for dx, dy in itertools.product((-1, 0, 1), repeat=2):
        if (dx, dy) != (0, 0):
            yield x+dx, y+dy 

def show_set(s):
    xs = [p[0] for p in s]
    ys = [p[1] for p in s]
    x_range = list(range(min(xs), max(xs) + 1))
    y_range = list(range(min(ys), max(ys) + 1))
    for x in x_range:
        print("".join(("#" if (x, y) in s else " ") for y in y_range) + "    " + str(x))
    print("".join(str(y%10) for y in y_range))
    print()


def play_rounds(elves, nb_round):
    attempts = collections.deque(attempts_original)
    show_set(elves)
    for _ in range(nb_round):
        proposals = dict()
        elves2 = set()
        for x, y in elves:
            if not any(n in elves for n in neighbours((x, y))):
                elves2.add((x, y))
            else:
                for a in attempts:
                    candidates = [(x+dx, y+dy) for dx, dy in a]
                    if not any(c in elves for c in candidates):
                        proposals.setdefault(candidates[0], []).append((x, y))
                        break
                else:
                    elves2.add((x, y))
        for pos, lst in proposals.items():
            if len(lst) > 1:
                for e in lst:
                    assert e not in elves2
                    elves2.add(e)
            else:
                assert pos not in elves2
                elves2.add(pos)
        attempts.rotate(-1)
        assert len(elves) == len(elves2)
        elves = elves2
        # show_set(elves)
    xs = [p[0] for p in elves]
    ys = [p[1] for p in elves]
    return (1 + max(xs) - min(xs)) * (1 + max(ys) - min(ys)) - len(elves)

def run_tests():
    elves = get_elves_from_lines(""".....
..##.
..#..
.....
..##.
.....""")
    play_rounds(elves, 3)
    elves = get_elves_from_lines("""..............
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
..............""")
    assert play_rounds(elves, 10) == 110


def get_solutions():
    elves = get_elves_from_file()
    print(play_rounds(elves, 10))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
