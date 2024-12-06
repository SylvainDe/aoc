# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_component_from_line(string):
    sep = ": "
    name, mid, lst = string.partition(sep)
    assert mid == sep
    return name, lst.split()


def get_components_from_lines(string):
    return [get_component_from_line(l) for l in string.splitlines()]


def get_components_from_file(file_path=top_dir + "resources/year2023_day25_input.txt"):
    with open(file_path) as f:
        return get_components_from_lines(f.read())


def separate_in_2_groups(components):
    links = set()
    for n1, lst in components:
        for n2 in lst:
            links.add((n1, n2))
    print(links)


def run_tests():
    components = get_components_from_lines(
        """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr"""
    )
    print(separate_in_2_groups(components))


def get_solutions():
    components = get_components_from_file()
    # print(components)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
