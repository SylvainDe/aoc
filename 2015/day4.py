# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import itertools
import hashlib


def get_key_from_file(file_path="day4_input.txt"):
    with open(file_path) as f:
        for l in f:
            return l.strip()


def get_coin(key, nb_zeros=5):
    zeros = "0" * nb_zeros
    for i in itertools.count():
        s = key + str(i)
        h = hashlib.md5(s.encode("utf-8")).hexdigest()
        if h.startswith(zeros):
            return i


def run_tests():
    assert get_coin("abcdef") == 609043
    assert get_coin("pqrstuv") == 1048970


def get_solutions():
    key = get_key_from_file()
    print(get_coin(key))
    print(get_coin(key, 6))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
