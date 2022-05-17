# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import re
import collections

left_re = r"(.*) \((\d+)\)"


def get_program_from_string(s):
    left, mid, right = s.partition(" -> ")
    lst = right.split(", ") if right else []
    name, weight = re.match(left_re, left).groups()
    return name, (int(weight), lst)


def get_prog_from_file(file_path="../../resources/year2017_day7_input.txt"):
    with open(file_path) as f:
        return dict(get_program_from_string(l.strip()) for l in f)


def get_bottom(programs):
    parents = dict()
    for name, (_, lst) in programs.items():
        for e in lst:
            assert e not in parents
            parents[e] = name
    bottoms = list(programs.keys() - parents)
    assert len(bottoms) == 1
    return bottoms[0]


def get_wrong_disc(programs):
    unweighted_programs = dict(programs)
    weights = dict()
    disk_weights = dict()
    while unweighted_programs:
        for name, (weight, lst) in unweighted_programs.items():
            subweights_dict = {p: weights.get(p, None) for p in lst}
            subweights = subweights_dict.values()
            if not all(subweights):
                continue
            c = collections.Counter(subweights)
            if len(c) > 1:
                # If we have more than 1 weight, we expect a most common one to be correct and another one to exist only once and be wrong
                (mc, nb_mc), (lc, nb_lc) = c.most_common()
                assert nb_lc == 1
                # Compute the desired weight based on the actual weight
                for p, w in subweights_dict.items():
                    if w == lc:
                        return disk_weights[p] + mc - lc
                else:
                    assert False, "Did not find weight"
            disk_weights[name] = weight
            weights[name] = weight + sum(subweights)
            unweighted_programs.pop(name)
            break
        else:  # no break
            assert False, "Cannot compute remaining weights"


def run_tests():
    prog = [
        "pbga (66)",
        "xhth (57)",
        "ebii (61)",
        "havc (66)",
        "ktlj (57)",
        "fwft (72) -> ktlj, cntj, xhth",
        "qoyq (66)",
        "padx (45) -> pbga, havc, qoyq",
        "tknk (41) -> ugml, padx, fwft",
        "jptl (61)",
        "ugml (68) -> gyxo, ebii, jptl",
        "gyxo (61)",
        "cntj (57)",
    ]
    prog = dict(get_program_from_string(s) for s in prog)
    assert get_bottom(prog) == "tknk"
    assert get_wrong_disc(prog) == 60


def get_solutions():
    prog = get_prog_from_file()
    print(get_bottom(prog))
    print(get_wrong_disc(prog))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
