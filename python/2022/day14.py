# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import itertools

def get_segments_from_line(string):
    return [tuple(int(c) for c in c.split(",")) for c in string.split(" -> ")]

def get_segments_from_lines(string):
    return [get_segments_from_line(l) for l in string.splitlines()]

def get_segments_from_file(file_path="../../resources/year2022_day14_input.txt"):
    with open(file_path) as f:
        return get_segments_from_lines(f.read())

def get_rocks(segments):
    rocks = set()
    for l in segments:
        for (x_p, y_p), (x_n, y_n) in zip(l, l[1:]):
            if x_p == x_n:
                mini, maxi = sorted((y_p, y_n))
                for y in range(mini, maxi + 1):
                    rocks.add((x_p, y))
            elif y_p == y_n:
                mini, maxi = sorted((x_p, x_n))
                for x in range(mini, maxi + 1):
                    rocks.add((x, y_p))
            else:
                assert False
    return rocks

def get_candidate_positions(pos):
    x, y = pos
    return ((x, y+1), (x-1, y+1), (x+1, y+1))

def drop_sand(segments, is_part1):
    rocks = get_rocks(segments)
    rock_bottom = max(y for (x, y) in rocks)
    if not is_part1:
        for x in range(-1000, 1000):
            rocks.add((x, rock_bottom+2))
    for i in itertools.count():
        pos = (500, 0)
        if pos in rocks:
            assert not is_part1
            return i
        while True:
            for pos2 in get_candidate_positions(pos):
                if pos2 not in rocks:
                    pos = pos2
                    if is_part1 and pos[1] > rock_bottom:
                        return i
                    break
            else:
                rocks.add(pos)
                break

def run_tests():
    segments = get_segments_from_lines("""498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9""")
    assert drop_sand(segments, is_part1=True) == 24
    assert drop_sand(segments, is_part1=False) == 93

def get_solutions():
    segments = get_segments_from_file()
    print(drop_sand(segments, is_part1=True) == 825)
    print(drop_sand(segments, is_part1=False) == 26729)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
