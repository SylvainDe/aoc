# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"

def get_range_from_string(string, sep="-"):
    left, mid, right = string.partition(sep)
    assert mid == sep
    return int(left), int(right)


def get_ranges_from_line(string):
    return [get_range_from_string(s) for s in string.split(",")]


def get_ranges_from_file(file_path=top_dir + "resources/year2025_day2_input.txt"):
    with open(file_path) as f:
        for l in f:
            return get_ranges_from_line(l.strip())


def get_invalids(range_, only_2_rep):
    l, r = range_
    l_str, r_str = str(l), str(r)
    for nb_rep in [2] if only_2_rep else range(2, 1 + len(r_str)):
        mini = l_str[:len(l_str)//nb_rep]
        maxi = r_str[:1+len(r_str)//nb_rep]
        for i in range(int(mini) if mini else 0, int(maxi) + 1):
            i_str = str(i)
            v = int(i_str * nb_rep)
            if l <= v <= r:
                yield v


def get_invalids_sum(ranges, only_2_rep):
    return sum(sum(set(get_invalids(r, only_2_rep=only_2_rep))) for r in ranges)


def run_tests():
    assert list(get_invalids((11, 22), only_2_rep=True)) == [11, 22]
    assert list(get_invalids((95, 115), only_2_rep=True)) == [99]
    ranges = get_ranges_from_line("11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124")
    assert get_invalids_sum(ranges, only_2_rep=True) == 1227775554
    assert list(get_invalids((11, 22), only_2_rep=False)) == [11, 22]
    assert list(get_invalids((2121212118, 2121212124), only_2_rep=False)) == [2121212121]
    assert get_invalids_sum(ranges, only_2_rep=False) == 4174379265

def get_solutions():
    ranges = get_ranges_from_file()
    print(get_invalids_sum(ranges, only_2_rep=True) == 12599655151)
    print(get_invalids_sum(ranges, only_2_rep=False) == 20942028255)



if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
