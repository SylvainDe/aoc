# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import functools
import operator


def get_nbs_from_hex_str(string):
    l = [ord(c) for c in string] + [17, 31, 73, 47, 23]
    return l * 64


def lst_to_hexa(lst):
    args16 = [iter(lst)] * 16
    hexs = [
        hex(functools.reduce(operator.xor, val16))[2:].zfill(2)
        for val16 in zip(*args16)
    ]
    return "".join(hexs)


def compute_knot_hash_internal(nb_elt, lengths):
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
    return lst


def knot_hash(string):
    lengths = get_nbs_from_hex_str(string)
    return lst_to_hexa(compute_knot_hash_internal(256, lengths))


def run_tests():
    assert (
        get_nbs_from_hex_str("1,2,3") == [49, 44, 50, 44, 51, 17, 31, 73, 47, 23] * 64
    )
    assert knot_hash("") == "a2582a3a0e66e6e86e3812dcb672a272"
    assert knot_hash("AoC 2017") == "33efeb34ea91902bb2f59c9920caa6cd"
    assert knot_hash("1,2,3") == "3efbe78a8d82f29979031a4aa0b16a9d"
    assert knot_hash("1,2,4") == "63960835bcdc130f0b66d7ff4f6a5a8e"


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    end = datetime.datetime.now()
    print(end - begin)
