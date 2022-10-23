# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_freq_from_file(file_path="../../resources/year2018_day1_input.txt"):
    with open(file_path) as f:
        return [int(l.strip()) for l in f]


def get_resulting_freq(freqs):
    return sum(freqs)


def get_first_repetition(freqs):
    freq = 0
    seens = set([freq])
    while True:
        for f in freqs:
            freq += f
            if freq in seens:
                return freq
            seens.add(freq)


def run_tests():
    assert get_resulting_freq([+1, -2, +3, +1]) == 3
    assert get_first_repetition([+1, -2, +3, +1]) == 2


def get_solutions():
    freqs = get_freq_from_file()
    print(get_resulting_freq(freqs))
    print(get_first_repetition(freqs))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
