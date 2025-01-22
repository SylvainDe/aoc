# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import itertools

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_signal_from_line(string):
    return [int(c) for c in string]


def get_signal_from_file(file_path=top_dir + "resources/year2019_day16_input.txt"):
    with open(file_path) as f:
        for l in f:
            return get_signal_from_line(l.strip())


def next_signal(signal):
    s = []
    for i, v in enumerate(signal, start=1):
        pattern = itertools.cycle(sum(([v] * i for v in (0, 1, 0, -1)), []))
        next(pattern)
        s.append(abs(sum([p * s for p, s in zip(pattern, signal)])) % 10)
    return s


def nth_signal(n, signal):
    for _ in range(n):
        signal = next_signal(signal)
    return signal


def format_lst(lst):
    return "".join(str(c) for c in lst)


def run_tests():
    signal = get_signal_from_line("12345678")
    assert format_lst(next_signal(signal)) == "48226158"
    assert format_lst(nth_signal(4, signal)) == "01029498"
    assert (
        format_lst(
            nth_signal(100, get_signal_from_line("80871224585914546619083218645595"))[
                :8
            ]
        )
        == "24176176"
    )
    assert (
        format_lst(
            nth_signal(100, get_signal_from_line("19617804207202209144916044189917"))[
                :8
            ]
        )
        == "73745418"
    )
    assert (
        format_lst(
            nth_signal(100, get_signal_from_line("69317163492948606335995924319873"))[
                :8
            ]
        )
        == "52432133"
    )


def get_solutions():
    signal = get_signal_from_file()
    print(format_lst(nth_signal(100, signal)[:8]))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
