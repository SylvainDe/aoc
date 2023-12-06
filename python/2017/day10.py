# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import functools
import operator


resource_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../resources/"

def get_first_line(file_path=resource_dir + "year2017_day10_input.txt"):
    with open(file_path) as f:
        for l in f:
            return l.strip()


def get_nb_lst(string, is_part1):
    if is_part1:
        return [int(s) for s in string.split(",")]
    else:
        l = [ord(c) for c in string] + [17, 31, 73, 47, 23]
        return l * 64


def process(nb_elt, string, is_part1=True):
    lengths = get_nb_lst(string, is_part1)
    lst = list(range(nb_elt))
    curr_pos = 0
    skip_size = 0
    for leng in lengths:
        beg, end = curr_pos, curr_pos + leng
        assert 0 <= beg < nb_elt
        if end < nb_elt:
            # Normal case
            assert 0 <= beg <= end < nb_elt
            src = list(reversed(lst[beg:end]))
            assert len(src) == leng
            lst[beg:end] = src
        else:
            # Wrap-around case
            end -= nb_elt
            assert 0 <= end <= beg < nb_elt
            src1, src2 = lst[beg:], lst[:end]
            src = list(reversed(src1 + src2))
            assert len(src) == leng
            dst1, dst2 = src[: nb_elt - beg], src[nb_elt - beg :]
            assert src == dst1 + dst2
            assert len(src1) == len(dst1)
            assert len(src2) == len(dst2)
            lst[beg:], lst[:end] = dst1, dst2
        curr_pos = (curr_pos + leng + skip_size) % nb_elt
        skip_size += 1
    if is_part1:
        return lst[0] * lst[1]
    else:
        args16 = [iter(lst)] * 16
        hexs = [
            hex(functools.reduce(operator.xor, val16))[2:].zfill(2)
            for val16 in zip(*args16)
        ]
        return "".join(hexs)


def run_tests():
    is_part1 = True
    assert get_nb_lst("3,4,1,5", is_part1) == [3, 4, 1, 5]
    assert process(5, "3,4,1,5", is_part1) == 12
    is_part1 = False
    assert (
        get_nb_lst("1,2,3", is_part1) == [49, 44, 50, 44, 51, 17, 31, 73, 47, 23] * 64
    )
    assert process(256, "", is_part1) == "a2582a3a0e66e6e86e3812dcb672a272"
    assert process(256, "AoC 2017", is_part1) == "33efeb34ea91902bb2f59c9920caa6cd"
    assert process(256, "1,2,3", is_part1) == "3efbe78a8d82f29979031a4aa0b16a9d"
    assert process(256, "1,2,4", is_part1) == "63960835bcdc130f0b66d7ff4f6a5a8e"


def get_solutions():
    s = get_first_line()
    print(process(256, s, is_part1=True) == 48705)
    print(process(256, s, is_part1=False) == "1c46642b6f2bc21db2a2149d0aeeae5d")


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
