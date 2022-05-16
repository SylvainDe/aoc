# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import itertools


def get_numbers_from_file(file_path="day15_input.txt"):
    with open(file_path) as f:
        for l in f:
            return [int(s) for s in l.split(",")]


def yield_game(numbers):
    turns = dict()
    for turn, n in enumerate(numbers):
        turns.setdefault(n, []).append(turn)
        yield n
    for turn in itertools.count(start=turn + 1):
        lst = turns[n]
        n = (lst[-1] - lst[-2]) if len(lst) > 1 else 0
        turns.setdefault(n, []).append(turn)
        yield n


def n_th(n, it):
    for i, v in enumerate(it):
        if i == n:
            return v


def play_game(numbers, turn):
    return n_th(turn - 1, yield_game(numbers))


def run_tests():
    example1 = [0, 3, 6]
    assert list(itertools.islice(yield_game(example1), 10)) == [
        0,
        3,
        6,
        0,
        3,
        3,
        1,
        0,
        4,
        0,
    ]
    assert play_game(example1, 1) == 0
    assert play_game(example1, 9) == 4
    assert play_game(example1, 10) == 0
    assert play_game(example1, 2020) == 436
    assert play_game([1, 3, 2], 2020) == 1
    assert play_game([2, 1, 3], 2020) == 10
    assert play_game([1, 2, 3], 2020) == 27
    assert play_game([2, 3, 1], 2020) == 78
    assert play_game([3, 2, 1], 2020) == 438
    assert play_game([3, 1, 2], 2020) == 1836
    # assert play_game(example1, 30000000) == 175594 # Slow


def get_solutions():
    numbers = get_numbers_from_file()
    print(play_game(numbers, 2020) == 273)
    # print(play_game(numbers, 30000000) == 47205) # Slow


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
