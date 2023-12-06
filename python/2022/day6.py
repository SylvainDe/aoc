# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


resource_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../resources/"


def get_signal_from_file(file_path=resource_dir + "year2022_day6_input.txt"):
    with open(file_path) as f:
        for l in f:
            return l
    return None


def get_marker(signal, winsize):
    for i in range(len(signal)):
        if len(set(signal[i : i + winsize])) == winsize:
            return i + winsize
    return None


def run_tests():
    assert get_marker("mjqjpqmgbljsphdztnvjfqwrcgsmlb", winsize=4) == 7
    assert get_marker("bvwbjplbgvbhsrlpgdmjqwftvncz", winsize=4) == 5
    assert get_marker("nppdvjthqldpwncqszvftbrmjlhg", winsize=4) == 6
    assert get_marker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", winsize=4) == 10
    assert get_marker("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", winsize=4) == 11
    assert get_marker("mjqjpqmgbljsphdztnvjfqwrcgsmlb", winsize=14) == 19
    assert get_marker("bvwbjplbgvbhsrlpgdmjqwftvncz", winsize=14) == 23
    assert get_marker("nppdvjthqldpwncqszvftbrmjlhg", winsize=14) == 23
    assert get_marker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", winsize=14) == 29
    assert get_marker("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", winsize=14) == 26


def get_solutions():
    signal = get_signal_from_file()
    print(get_marker(signal, winsize=4) == 1850)
    print(get_marker(signal, winsize=14) == 2823)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
