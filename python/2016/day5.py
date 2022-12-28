# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import hashlib
import itertools


def get_door_id_from_file(file_path="../../resources/year2016_day5_input.txt"):
    with open(file_path) as f:
        for l in f:
            return l.strip()


def yield_hashes(door_id, nb_zeros):
    zeros = "0" * nb_zeros
    for i in itertools.count():
        val = door_id + str(i)
        h = hashlib.md5(val.encode("utf-8")).hexdigest()
        if h.startswith(zeros):
            yield h[nb_zeros:]


def compute_password(door_id, length=8, nb_zeros=5):
    return "".join(
        h[0] for h in itertools.islice(yield_hashes(door_id, nb_zeros), length)
    )


def compute_password2(door_id, length=8, nb_zeros=5):
    password = [None] * length
    for h in yield_hashes(door_id, nb_zeros):
        position, value = h[0], h[1]
        if "0" <= position <= "7":
            position_int = int(position)
            if password[position_int] is None:
                password[position_int] = value
                if None not in password:
                    return "".join(password)


def run_tests():
    door_id = "abc"
    assert compute_password(door_id) == "18f47a30"
    assert compute_password2(door_id) == "05ace8e3"


def get_solutions():
    door_id = get_door_id_from_file()
    print(compute_password(door_id) == "c6697b55")
    print(compute_password2(door_id) == "8c35d1ab")


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
