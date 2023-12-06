# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import math


resource_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../resources/"

def get_info_from_file(file_path=resource_dir + "year2020_day13_input.txt"):
    with open(file_path) as f:
        return get_time_and_buses(*[l for l in f])


def get_time_and_buses(line1, line2):
    return int(line1), [None if s == "x" else int(s) for s in line2.split(",")]


def get_wait_time_for_bus(time, freq):
    return freq - (time % freq)


def get_next_bus(time, buses):
    return min((get_wait_time_for_bus(time, b), b) for b in buses if b is not None)


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


def get_next_timestamp_with_offsets(buses):
    buses = [(idx, freq) for idx, freq in enumerate(buses) if freq is not None]
    time = 0
    step = 1
    for idx, freq in buses:
        # We want to reach a time t such that:
        # t+idx = k*freq by starting from "time" with steps of "step"
        # That is: time + idx + y*step = x*freq with x, y integers
        # Or: time + idx = y*freq - x*step
        # which could be written/solved with Euclidian algorithm
        # but it is not worth the pain
        if (time + idx) % math.gcd(step, freq):
            return None
        while True:
            if (time + idx) % freq == 0:
                break
            time += step
        step = lcm(step, freq)
    return time


def run_tests():
    example1 = ["939", "7,13,x,x,59,x,31,19"]
    time, buses = get_time_and_buses(example1[0], example1[1])
    wait, nb = get_next_bus(time, buses)
    assert (nb, wait) == (59, 5)
    assert nb * wait == 295
    assert get_next_timestamp_with_offsets(buses) == 1068781
    assert get_next_timestamp_with_offsets([17, None, 13, 19]) == 3417
    assert get_next_timestamp_with_offsets([67, 7, 59, 61]) == 754018
    assert get_next_timestamp_with_offsets([67, None, 7, 59, 61]) == 779210
    assert get_next_timestamp_with_offsets([67, 7, None, 59, 61]) == 1261476
    assert get_next_timestamp_with_offsets([1789, 37, 47, 1889]) == 1202161486
    # My own tests
    assert get_next_timestamp_with_offsets([2, None, 4]) == 2
    assert get_next_timestamp_with_offsets([2, 4]) is None


def get_solutions():
    time, buses = get_info_from_file()
    wait, nb = get_next_bus(time, buses)
    print(nb * wait == 2845)
    print(get_next_timestamp_with_offsets(buses) == 487905974205117)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
