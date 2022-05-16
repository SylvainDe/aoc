# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_depths_from_file(file_path="day1_input.txt"):
    with open(file_path) as f:
        return [int(l.strip()) for l in f]


def get_nb_increments(depths, windowsize=1):
    # Window(n + 1) > Window(n)
    # d(n+1) + d(n+2) + ... + d(n+1+windowsize) > d(n) + d(n+1) + ... + d(n+windowsize)
    # d(n+1+windowsize) > d(n)
    return sum(last > first for first, last in zip(depths, depths[windowsize:]))


def run_tests():
    depths = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
    assert get_nb_increments(depths) == 7
    assert get_nb_increments(depths, 3) == 5


def get_solutions():
    depths = get_depths_from_file()
    print(get_nb_increments(depths))
    print(get_nb_increments(depths, 3))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
