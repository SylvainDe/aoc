# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_nb_from_line(string):
    return [int(s) for s in string.split(",")]


def get_nb_from_file(file_path="../../resources/year2017_day10_input.txt"):
    with open(file_path) as f:
        for l in f:
            return get_nb_from_line(l.strip())


def process(nb_elt, lengths):
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
            dst1, dst2 = src[:nb_elt - beg], src[nb_elt-beg:]
            assert src == dst1 + dst2
            assert len(src1) == len(dst1)
            assert len(src2) == len(dst2)
            lst[beg:], lst[:end] = dst1, dst2
        curr_pos = (curr_pos + leng + skip_size) % nb_elt
        skip_size += 1
    return lst[0] * lst[1]


def run_tests():
    lengths = get_nb_from_line("3,4,1,5")
    assert process(5, lengths) == 12


def get_solutions():
    lengths = get_nb_from_file()
    print(process(256, lengths) == 48705)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
