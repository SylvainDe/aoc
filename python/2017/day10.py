# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import knot_hash

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_first_line(file_path=top_dir + "resources/year2017_day10_input.txt"):
    with open(file_path) as f:
        for l in f:
            return l.strip()


def get_nbs_from_comma_separated_str(string):
    return [int(s) for s in string.split(",")]


def day10_part1(nb_elt, string):
    lengths = get_nbs_from_comma_separated_str(string)
    lst = knot_hash.compute_knot_hash_internal(nb_elt, lengths)
    return lst[0] * lst[1]


def run_tests():
    assert get_nbs_from_comma_separated_str("3,4,1,5") == [3, 4, 1, 5]
    assert day10_part1(5, "3,4,1,5") == 12


def get_solutions():
    s = get_first_line()
    print(day10_part1(256, s) == 48705)
    print(knot_hash.knot_hash(s) == "1c46642b6f2bc21db2a2149d0aeeae5d")


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
