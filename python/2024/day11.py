# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_stones_from_line(string):
    return [int(n) for n in string.split()]


def get_stones_from_file(file_path=top_dir + "resources/year2024_day11_input.txt"):
    with open(file_path) as f:
        for l in f:
            return get_stones_from_line(l.strip())


def get_next_steps(s):
    if s == 0:
        yield 1
        return
    s_str = str(s)
    l = len(s_str)
    q, r = divmod(l, 2)
    if r == 0:
        yield int(s_str[:q])
        yield int(s_str[q:])
    else:
        yield 2024 * s


def blink(stones):
    return [s2 for s in stones for s2 in get_next_steps(s)]


def blink_n(stones, n):
    for i in range(n):
        print(i)
        stones = blink(stones)
    return len(stones)


def run_tests():
    stones = get_stones_from_line("0 1 10 99 999")
    assert blink(stones) == [1, 2024, 1, 0, 9, 9, 2021976]
    stones = get_stones_from_line("125 17")
    assert blink_n(stones, 6) == 22
    assert blink_n(stones, 25) == 55312


def get_solutions():
    stones = get_stones_from_file()
    print(blink_n(stones, 25))
    # print(blink_n(stones, 75))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
