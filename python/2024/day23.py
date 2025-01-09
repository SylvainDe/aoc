# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import itertools

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_conn_from_line(string):
    sep = "-"
    beg, mid, end = string.partition(sep)
    assert mid == sep
    return beg, end


def get_conns_from_lines(string):
    return [get_conn_from_line(l) for l in string.splitlines()]


def get_conns_from_file(file_path=top_dir + "resources/year2024_day23_input.txt"):
    with open(file_path) as f:
        return get_conns_from_lines(f.read())


def get_conns_as_dict(conns):
    conn_dict = dict()
    for a, b in conns:
        conn_dict.setdefault(a, set()).add(b)
        conn_dict.setdefault(b, set()).add(a)
    return conn_dict


def get_interconnected_triples(conns):
    conns = get_conns_as_dict(conns)
    for cpu, lst in conns.items():
        lst2 = [c for c in lst if c > cpu]
        for cpu2, cpu3 in itertools.combinations(lst2, 2):
            conn2 = cpu2 in conns[cpu3]
            conn3 = cpu3 in conns[cpu2]
            assert conn2 == conn3
            if conn2:
                yield cpu, cpu2, cpu3


def intersection(sets):
    sets = list(sets)
    if not sets:
        return set()
    ret = sets[0]
    for s in sets[1:]:
        ret = ret.intersection(s)
    return ret


def get_interconnected_set(conns):
    conns = get_conns_as_dict(conns)
    sets = [[cpu] for cpu in conns.keys()]
    for i in itertools.count(1):
        new_sets = []
        for s in sets:
            assert len(s) == i
            cands = intersection(conns[cpu] for cpu in s)
            for c in cands:
                if c > s[-1]:
                    new_sets.append(s + [c])
        if new_sets:
            sets = new_sets
        else:
            return ",".join(sets[0])


def run_tests():
    conns = get_conns_from_lines(
        """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""
    )
    ret = list(get_interconnected_triples(conns))
    assert len(ret) == 12
    ret2 = [s for s in ret if any(e.startswith("t") for e in s)]
    assert len(ret2) == 7
    assert get_interconnected_set(conns) == "co,de,ka,ta"


def get_solutions():
    conns = get_conns_from_file()
    print(
        len(
            [
                s
                for s in get_interconnected_triples(conns)
                if any(e.startswith("t") for e in s)
            ]
        )
        == 1248
    )
    print(get_interconnected_set(conns) == "aa,cf,cj,cv,dr,gj,iu,jh,oy,qr,xr,xy,zb")


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
