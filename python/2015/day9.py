# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import re

info_re = r"^(?P<loc1>[A-Za-z]+) to (?P<loc2>[A-Za-z]+) = (?P<dist>\d+)$"


def get_info_from_str(s):
    match = re.match(info_re, s)
    d = match.groupdict()
    return d["loc1"], d["loc2"], int(d["dist"])


def get_info_from_file(file_path="../../resources/year2015_day9_input.txt"):
    with open(file_path) as f:
        return [get_info_from_str(l.strip()) for l in f]


def build_graph(info):
    g = dict()
    for loc1, loc2, d in info:
        g.setdefault(loc1, dict())[loc2] = d
        g.setdefault(loc2, dict())[loc1] = d
    return g


def get_routes(graph):
    paths = [([loc], 0) for loc in graph]
    for _ in range(len(graph) - 1):
        paths2 = []
        for path, d in paths:
            last = path[-1]
            for loc2, d2 in graph[last].items():
                if loc2 not in path:
                    paths2.append((path + [loc2], d + d2))
        paths = paths2
    return paths


def run_tests():
    info = [
        "London to Dublin = 464",
        "London to Belfast = 518",
        "Dublin to Belfast = 141",
    ]
    info = [get_info_from_str(s) for s in info]
    graph = build_graph(info)
    routes = get_routes(graph)
    assert min(d for path, d in routes) == 605
    assert max(d for path, d in routes) == 982


def get_solutions():
    info = get_info_from_file()
    graph = build_graph(info)
    routes = get_routes(graph)
    print(min(d for path, d in routes) == 207)
    print(max(d for path, d in routes) == 804)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
