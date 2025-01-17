# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import itertools

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_block_from_line(string):
    return tuple(int(v) for v in string.split(","))


def get_blocks_from_lines(string):
    return [get_block_from_line(l) for l in string.splitlines()]


def get_blocks_from_file(file_path=top_dir + "resources/year2024_day18_input.txt"):
    with open(file_path) as f:
        return get_blocks_from_lines(f.read())


def display(blocks, xs=None, ys=None):
    if not blocks:
        print("Empty")
        return
    if xs is None:
        xs = set(x for x, _ in blocks)
    if ys is None:
        ys = set(y for _, y in blocks)
    for y in range(min(ys), max(ys) + 1):
        print(
            "".join(
                "#" if (x, y) in blocks else " " for x in range(min(xs), max(xs) + 1)
            )
        )


def display2(d, xs=None, ys=None):
    if not d:
        print("Empty")
        return
    if xs is None:
        xs = set(x for x, _ in d.keys())
    if ys is None:
        ys = set(y for _, y in d.keys())
    for y in range(min(ys), max(ys) + 1):
        print("".join(d.get((x, y), " ") for x in range(min(xs), max(xs) + 1)))


def get_neighbours(pos):
    x, y = pos
    return ((x + dx, y + dy) for (dx, dy) in ((-1, 0), (+1, 0), (0, -1), (0, +1)))


def get_dist(size, blocks, start=None, end=None):
    if start is None:
        start = 0, 0
    if end is None:
        end = size - 1, size - 1
    side = list(range(size))
    seen = set()
    reach = set([start])
    for i in itertools.count():
        if not reach:
            return None
        reach2 = set()
        for p in reach:
            if p == end:
                return i
            if p in seen:
                continue
            seen.add(p)
            for p2 in get_neighbours(p):
                if (
                    all(0 <= c < size for c in p2)
                    and p2 not in blocks
                    and p2 not in seen
                ):
                    reach2.add(p2)
        reach = reach2


def find_blocking_block(size, blocks):
    blocks2 = set()
    for i, b in enumerate(blocks):
        blocks2.add(b)
        if get_dist(size, blocks2) is None:
            return b


def run_tests():
    size = 7
    blocks = get_blocks_from_lines(
        """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""
    )
    blocks12 = set(blocks[:12])
    assert get_dist(size, blocks12) == 22
    assert find_blocking_block(size, blocks) == (6, 1)


def get_solutions():
    size = 71
    blocks = get_blocks_from_file()
    blocks1024 = set(blocks[:1024])
    print(get_dist(size, blocks1024) == 356)
    # Slow
    # print(find_blocking_block(size, blocks) == (22, 33))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
