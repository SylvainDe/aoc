# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import hashlib
import itertools


def get_door_id_from_file(file_path="../../resources/year2016_day5_input.txt"):
    with open(file_path) as f:
        for l in f:
            return l.strip()

def yield_password_chars(door_id, nb_zeros):
    zeros = "0" * nb_zeros
    for i in itertools.count():
        val = door_id + str(i)
        h = hashlib.md5(val.encode("utf-8")).hexdigest()
        if h.startswith(zeros):
            yield h[nb_zeros]


def compute_password(door_id, length=8, nb_zeros=5):
    return "".join(itertools.islice(yield_password_chars(door_id, nb_zeros), length))


def run_tests():
    door_id = "abc"
    assert compute_password(door_id) == "18f47a30"


def get_solutions():
    door_id = get_door_id_from_file()
    print(compute_password(door_id))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
