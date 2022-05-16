# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_map_item_from_line(l, sep="-"):
    a, b, c = l.partition(sep)
    assert b == sep
    return (a, c)


def get_map_from_lines(lines):
    return [get_map_item_from_line(l.strip()) for l in lines]


def get_map_from_file(file_path="day12_input.txt"):
    with open(file_path) as f:
        return get_map_from_lines(f)


def build_graph(map_):
    graph = dict()
    for a, b in map_:
        graph.setdefault(a, set()).add(b)
        graph.setdefault(b, set()).add(a)
    return graph


def get_nb_paths(graph, nb_double_visit=0, start="start", end="end"):
    # I suspect there is a much better way using dynamic programming
    nb_path = 0
    paths = [(start, set([start]), 0)]  # last, visited, double_visit
    while paths:
        last, visited, double_visit = paths.pop()
        for succ in graph.get(last, set()):
            if succ == end:
                nb_path += 1
            elif succ.isupper():
                paths.append((succ, visited, double_visit))
            elif succ not in visited:
                paths.append((succ, visited | set([succ]), double_visit))
            elif succ != start and nb_double_visit >= double_visit + 1:
                paths.append((succ, visited, double_visit + 1))
    return nb_path


def run_tests():
    map_ = [
        "start-A",
        "start-b",
        "A-c",
        "A-b",
        "b-d",
        "A-end",
        "b-end",
    ]
    map_ = get_map_from_lines(map_)
    graph = build_graph(map_)
    assert get_nb_paths(graph) == 10
    assert get_nb_paths(graph, 1) == 36
    map_ = [
        "dc-end",
        "HN-start",
        "start-kj",
        "dc-start",
        "dc-HN",
        "LN-dc",
        "HN-end",
        "kj-sa",
        "kj-HN",
        "kj-dc",
    ]
    map_ = get_map_from_lines(map_)
    graph = build_graph(map_)
    assert get_nb_paths(graph) == 19
    assert get_nb_paths(graph, 1) == 103
    map_ = [
        "fs-end",
        "he-DX",
        "fs-he",
        "start-DX",
        "pj-DX",
        "end-zg",
        "zg-sl",
        "zg-pj",
        "pj-he",
        "RW-he",
        "fs-DX",
        "pj-RW",
        "zg-RW",
        "start-pj",
        "he-WI",
        "zg-he",
        "pj-fs",
        "start-RW",
    ]
    map_ = get_map_from_lines(map_)
    graph = build_graph(map_)
    assert get_nb_paths(graph) == 226
    assert get_nb_paths(graph, 1) == 3509


def get_solutions():
    map_ = get_map_from_file()
    graph = build_graph(map_)
    print(get_nb_paths(graph))
    print(get_nb_paths(graph, 1))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
