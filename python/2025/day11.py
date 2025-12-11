# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import collections
import math

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_device_from_line(string):
    sep = ": "
    name, mid, outputs = string.partition(sep)
    assert mid == sep
    return name, tuple(outputs.split(" "))


def get_devices_from_lines(string):
    return dict(get_device_from_line(l) for l in string.splitlines())


def get_devices_from_file(file_path=top_dir + "resources/year2025_day11_input.txt"):
    with open(file_path) as f:
        return get_devices_from_lines(f.read())


def get_paths(devices, beg="you", end="out"):
    ret = 0
    paths = collections.Counter([beg])
    while paths:
        dev, nb = paths.popitem()
        if dev == end:
            ret += nb
        else:
            for out in devices.get(dev, ()):
                paths[out] += nb
    return ret


def get_paths2(devices):
    beg, end = "svr", "out"
    steps = ["dac", "fft"]
    ret = 0
    for order in [steps, list(reversed(steps))]:
        order = [beg] + order + [end]
        ret += math.prod(get_paths(devices, s1, s2) for s1, s2 in zip(order, order[1:]))
    return ret


def run_tests():
    devices = get_devices_from_lines(
        """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""
    )
    assert get_paths(devices) == 5
    devices = get_devices_from_lines(
        """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out""")
    assert get_paths2(devices) == 2


def get_solutions():
    devices = get_devices_from_file()
    print(get_paths(devices) == 749)
# NEEDS OPTIMISATION   print(get_paths2(devices))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
