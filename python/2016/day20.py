# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_range_from_str(s, sep="-"):
    left, mid, right = s.partition(sep)
    assert mid == sep
    return int(left), int(right)


def get_ip_range_from_file(file_path="../../resources/year2016_day20_input.txt"):
    with open(file_path) as f:
        return [get_range_from_str(l.strip()) for l in f]


def lowest_ip(ip_range):
    ip_range = sorted(ip_range)
    last_allowed = 0
    for beg, end in ip_range:
        if beg > last_allowed:
            break
        last_allowed = max(end + 1, last_allowed)
    return last_allowed


def nb_ip(ip_range, maxi):
    ip_range = sorted(ip_range)
    nb_ip = 0
    range_beg = 0
    for beg, end in ip_range:
        if beg > range_beg:
            nb_ip += beg - range_beg
        range_beg = max(end + 1, range_beg)
    if maxi > range_beg:
        nb_ip += maxi - range_beg
    return nb_ip


def run_tests():
    ip_range = [
        "5-8",
        "0-2",
        "4-7",
    ]
    ip_range = [get_range_from_str(s) for s in ip_range]
    assert lowest_ip(ip_range) == 3
    assert nb_ip(ip_range, 10) == 2


def get_solutions():
    ip_range = get_ip_range_from_file()
    print(lowest_ip(ip_range) == 19449262)
    print(nb_ip(ip_range, 4294967295) == 119)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
