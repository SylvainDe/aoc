# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import collections
import re
import itertools


# Filesystem              Size  Used  Avail  Use%
Node = collections.namedtuple(
    "Node", ("filesystem", "size", "used", "available", "percent_use")
)

# /dev/grid/node-x0-y0     85T   69T    16T   81%
node_re = r"^(?P<fs>[^ ]+) +(?P<size>\d+)T +(?P<used>\d+)T +(?P<avail>\d+)T +(?P<percent>\d+)%$"


def get_node_from_str(s):
    match = re.match(node_re, s)
    d = match.groupdict()
    return Node(
        d["fs"], int(d["size"]), int(d["used"]), int(d["avail"]), int(d["percent"])
    )


def get_nodes_from_file(file_path="../../resources/year2016_day22_input.txt"):
    with open(file_path) as f:
        lines = [l.strip() for l in f]
        return [get_node_from_str(s) for s in lines[2:]]


def run_tests():
    nodes = ""


def get_solutions():
    nodes = get_nodes_from_file()
    pairs = [
        (n1, n2)
        for n1, n2 in itertools.product(nodes, nodes)
        if n1.used != 0 and n1 != n2 and n1.used <= n2.available
    ]
    print(len(pairs) == 952)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
