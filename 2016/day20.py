# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_range_from_str(s, sep="-"):
    left, mid, right = s.partition(sep)
    assert mid == sep
    return int(left), int(right)


def get_ip_range_from_file(file_path="day20_input.txt"):
    with open(file_path) as f:
        return [get_range_from_str(l.strip()) for l in f]


def lowest_ip(ip_range):
    ip_range = sorted(ip_range)
    last_allowed = 0
    for beg, end in ip_range:
        if beg > last_allowed:
            break
        last_allowed = max(end+1, last_allowed)
    return last_allowed

def run_tests():
    ip_range = [
        "5-8",
        "0-2",
        "4-7",
    ]
    ip_range = [get_range_from_str(s) for s in ip_range]
    assert lowest_ip(ip_range) == 3

def get_solutions():
    ip_range = get_ip_range_from_file()
    print(lowest_ip(ip_range))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
