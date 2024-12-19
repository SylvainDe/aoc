# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_block_from_line(string):
    return tuple(int(v) for v in string.split(","))


def get_blocks_from_lines(string):
    return [get_block_from_line(l) for l in string.splitlines()]


def get_blocks_from_file(file_path=top_dir + "resources/year2024_day18_input.txt"):
    with open(file_path) as f:
        return get_blocks_from_lines(f.read())


def display(blocks):
    xs = set(x for x, _ in blocks)
    ys = set(y for _, y in blocks)
    for y in range(min(ys), max(ys) + 1):
        print(
            "".join(
                "#" if (x, y) in blocks else " " for x in range(min(xs), max(xs) + 1)
            )
        )


def run_tests():
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
    display(blocks12)


def get_solutions():
    blocks = get_blocks_from_file()
    blocks1024 = set(blocks[:1024])


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
