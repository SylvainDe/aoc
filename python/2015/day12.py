# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import json


resource_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../resources/"

def get_json_from_line(string):
    return json.loads(string)


def get_json_from_file(file_path=resource_dir + "year2015_day12_input.txt"):
    with open(file_path) as f:
        for l in f:
            return get_json_from_line(l.strip())


def sum_nb(obj, ignore_red):
    if isinstance(obj, str):
        return 0
    if isinstance(obj, int):
        return obj
    if isinstance(obj, list):
        return sum(sum_nb(e, ignore_red) for e in obj)
    if isinstance(obj, dict):
        if ignore_red and "red" in obj.values():
            return 0
        return sum(
            sum_nb(k, ignore_red) + sum_nb(v, ignore_red) for k, v in obj.items()
        )
    assert False


def run_tests():
    tests = [
        ("""[1,2,3]""", 6, 6),
        ("""{"a":2,"b":4}""", 6, 6),
        ("""[[[3]]]""", 3, 3),
        ("""{"a":{"b":4},"c":-1}""", 3, 3),
        ("""{"a":[-1,1]}""", 0, 0),
        ("""[-1,{"a":1}]""", 0, 0),
        ("""[]""", 0, 0),
        ("""{}""", 0, 0),
        ("""[1,{"c":"red","b":2},3]""", 6, 4),
        ("""{"d":"red","e":[1,2,3,4],"f":5}""", 15, 0),
        ("""[1,"red",5]""", 6, 6),
    ]
    for s, res1, res2 in tests:
        obj = get_json_from_line(s)
        assert sum_nb(obj, ignore_red=False) == res1
        assert sum_nb(obj, ignore_red=True) == res2


def get_solutions():
    obj = get_json_from_file()
    print(sum_nb(obj, ignore_red=False) == 119433)
    print(sum_nb(obj, ignore_red=True) == 68466)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
