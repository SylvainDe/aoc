# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_orbits_from_file(file_path="day6_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]


def build_graph(orbits):
    graph = dict()
    for orbit in orbits:
        left, right = orbit.split(")")
        graph[right] = left
    return graph


def get_path_to_com(graph, node):
    while node != "COM":
        yield node
        node = graph[node]


def count_distance(graph):
    return sum(len(list(get_path_to_com(graph, node))) for node in graph)


def distance_to_santa(graph):
    you_path = list(reversed(list(get_path_to_com(graph, "YOU"))))
    san_path = list(reversed(list(get_path_to_com(graph, "SAN"))))
    for i, (y, s) in enumerate(zip(you_path, san_path), start=1):
        if y != s:
            break
    return len(you_path) + len(san_path) - 2 * i


def run_tests():
    orbits = [
        "COM)B",
        "B)C",
        "C)D",
        "D)E",
        "E)F",
        "B)G",
        "G)H",
        "D)I",
        "E)J",
        "J)K",
        "K)L",
    ]
    graph = build_graph(orbits)
    assert count_distance(graph) == 42
    orbits = [
        "COM)B",
        "B)C",
        "C)D",
        "D)E",
        "E)F",
        "B)G",
        "G)H",
        "D)I",
        "E)J",
        "J)K",
        "K)L",
        "K)YOU",
        "I)SAN",
    ]
    graph = build_graph(orbits)
    assert distance_to_santa(graph) == 4


def get_solutions():
    orbits = get_orbits_from_file()
    graph = build_graph(orbits)
    print(count_distance(graph))
    print(distance_to_santa(graph))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
