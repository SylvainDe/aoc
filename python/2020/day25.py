# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import itertools


resource_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../resources/"

RUN_LONG_TESTS = False


def get_public_keys_from_file(file_path=resource_dir + "year2020_day25_input.txt"):
    with open(file_path) as f:
        return [int(l) for l in f]


MODULO = 20201227


def transform(subject_number, loop_size):
    return pow(subject_number, loop_size, MODULO)


def find_loop_size(subject_number, public_key):
    # There must be a better way
    v = 1
    for i in itertools.count(start=1):
        v = (v * subject_number) % MODULO
        if v == public_key:
            assert v == transform(subject_number, i)
            return i


def run_tests():
    pk1, pk2 = 5764801, 17807724
    ls1, ls2 = 8, 11
    key = 14897079
    assert transform(7, ls1) == pk1
    assert transform(7, ls2) == pk2
    assert find_loop_size(7, pk1) == ls1
    assert find_loop_size(7, pk2) == ls2
    assert transform(pk1, ls2) == key
    assert transform(pk2, ls1) == key


def get_solutions():
    pk1, pk2 = get_public_keys_from_file()
    if RUN_LONG_TESTS:
        ls1 = find_loop_size(7, pk1)
        ls2 = find_loop_size(7, pk2)
        print(transform(pk1, ls2) == 7269858)
        print(transform(pk2, ls1) == 7269858)


if __name__ == "__main__":
    RUN_LONG_TESTS = True
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
