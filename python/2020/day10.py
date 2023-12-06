# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import collections


resource_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../resources/"

def get_adapters_from_file(file_path=resource_dir + "year2020_day10_input.txt"):
    with open(file_path) as f:
        return [int(l) for l in f]


def get_jolt_differences(adapters):
    adapters = [0] + sorted(adapters) + [max(adapters) + 3]
    return collections.Counter(ad2 - ad1 for ad1, ad2 in zip(adapters, adapters[1:]))


def get_nb_charging_arrangements(adapters):
    adapters = [0] + sorted(adapters)
    nb_arr = []
    for i, ad in enumerate(adapters):
        nb = 0 if i else 1
        for idx in range(max(0, i - 3), i):
            if adapters[idx] + 3 >= ad:
                nb += nb_arr[idx]
        nb_arr.append(nb)
    return nb_arr[-1]


def run_tests():
    example1 = [16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4]
    example2 = [
        28,
        33,
        18,
        42,
        31,
        14,
        46,
        20,
        48,
        47,
        24,
        23,
        49,
        45,
        19,
        38,
        39,
        11,
        1,
        32,
        25,
        35,
        8,
        17,
        7,
        9,
        4,
        2,
        34,
        10,
        3,
    ]

    jolt_diff = get_jolt_differences(example1)
    assert jolt_diff[1] * jolt_diff[3] == 35
    jolt_diff = get_jolt_differences(example2)
    assert jolt_diff[1] * jolt_diff[3] == 220

    assert get_nb_charging_arrangements(example1) == 8
    assert get_nb_charging_arrangements(example2) == 19208


def get_solutions():
    adapters = get_adapters_from_file()
    jolt_diff = get_jolt_differences(adapters)
    print(jolt_diff[1] * jolt_diff[3] == 1656)
    print(get_nb_charging_arrangements(adapters) == 56693912375296)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
