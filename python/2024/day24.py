# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_simple_wire_from_line(string):
    beg, mid, end = string.partition(": ")
    return beg, int(end)


def get_complex_wire_from_line(string):
    lst = string.split(" ")
    return tuple(lst[i] for i in (4, 0, 1, 2))


def get_wires_from_lines(string):
    beg, mid, end = string.partition("\n\n")
    return [get_simple_wire_from_line(l) for l in beg.splitlines()], [
        get_complex_wire_from_line(l) for l in end.splitlines()
    ]


def get_wires_from_file(file_path=top_dir + "resources/year2024_day24_input.txt"):
    with open(file_path) as f:
        return get_wires_from_lines(f.read())


def evaluate_wires(wires):
    simp, comp = wires
    values = dict(simp)
    comp = {w: (w1, c, w2) for w, w1, c, w2 in comp}
    change = True
    while change:
        change = False
        for w, (w1, c, w2) in comp.items():
            assert w not in values
            w1val = values.get(w1)
            w2val = values.get(w2)
            nb_known = (w1val is not None) + (w2val is not None)
            wval = None
            if nb_known == 2:
                if c == "AND":
                    wval = w1val and w2val
                elif c == "OR":
                    wval = w1val or w2val
                elif c == "XOR":
                    wval = int(w1val != w2val)
            # elif nb_known == 1:
            #     knownval = w1val if w1val is not None else w2val
            #     if c == "AND":
            #         if knownval == 0:
            #             wval = 0
            #     elif c == "OR":
            #         if knownval == 1:
            #             wval = 1
            if wval is not None:
                values[w] = wval
                del comp[w]
                change = True
                break
    zkeys = sorted((k for k in values.keys() if k.startswith("z")), reverse=True)
    return int("".join(str(values[k]) for k in zkeys), 2)


def run_tests():
    wires = get_wires_from_lines(
        """x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02"""
    )
    assert evaluate_wires(wires) == 4
    wires = get_wires_from_lines(
        """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""
    )
    assert evaluate_wires(wires) == 2024


def get_solutions():
    wires = get_wires_from_file()
    print(evaluate_wires(wires) == 36035961805936)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
