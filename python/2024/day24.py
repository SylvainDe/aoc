# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import random

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_wire_value_from_line(string):
    beg, mid, end = string.partition(": ")
    return beg, int(end)


def get_gate_from_line(string):
    lst = string.split(" ")
    return tuple(lst[i] for i in (4, 0, 1, 2))


def get_wires_from_lines(string):
    beg, mid, end = string.partition("\n\n")
    return [get_wire_value_from_line(l) for l in beg.splitlines()], [
        get_gate_from_line(l) for l in end.splitlines()
    ]


def get_wires_from_file(file_path=top_dir + "resources/year2024_day24_input.txt"):
    with open(file_path) as f:
        return get_wires_from_lines(f.read())


def evaluate_wires(wires):
    wire_values, gates = wires
    return evaluate_wires_internal(gates, dict(wire_values))


def evaluate_wires_internal(gates, values):
    gates = {w: (w1, c, w2) for w, w1, c, w2 in gates}
    change = True
    while change:
        change = False
        for w, (w1, c, w2) in gates.items():
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
                del gates[w]
                change = True
                break
    zkeys = sorted((k for k in values.keys() if k.startswith("z")), reverse=True)
    return int("".join(str(values[k]) for k in zkeys), 2)


# Visually found wires
swaps = [("z11", "wpd"), ("skh", "jqf"), ("z19", "mdd"), ("z37", "wts")]


def find_wrong_wires_with_eval(gates):
    input_len = 45
    for i in range(10):
        a = random.randint(0, 2**input_len)
        b = random.randint(0, 2**input_len)
        c = a + b
        values = dict()
        for i in range(input_len):
            i2 = "{:02d}".format(i)
            values["x" + i2] = (a >> i) & 1
            values["y" + i2] = (b >> i) & 1
        d = evaluate_wires_internal(gates, values)
        if c != d:
            for i in range(input_len):
                ci = (c >> i) & 1
                di = (d >> i) & 1
                if ci != di:
                    print(a, b, c, d, i, ci, di)
                    break
            else:
                assert False


def extract_info(w):
    beg, end = w[0], w[1:]
    try:
        return int(end), beg
    except ValueError:
        return None, w


def find_swapped_wires_with_graphviz(wires):
    wire_values, gates = wires
    new_names = dict()
    wire_names = [c[0] for c in wire_values] + [c[0] for c in gates]
    # find_wrong_wires_with_eval(gates)
    # Swap visually found wires
    swap_dict = {}
    for w1, w2 in swaps:
        swap_dict[w1] = w2
        swap_dict[w2] = w1
    gates = [(swap_dict.get(w, w), w1, c, w2) for w, w1, c, w2 in gates]
    # find_wrong_wires_with_eval(gates)
    # Re-label wires
    new_names = {w: extract_info(w) for w in wire_names}
    renamed = True
    while renamed:
        renamed = False
        for w, w1, c, w2 in gates:
            n, l = new_names[w]
            if n is not None:
                continue
            inputs = [new_names[v] for v in (w1, w2)]
            if all(n is not None for n, _ in inputs):
                new_name = None
                inputs = sorted(inputs)
                (n1, l1), (n2, l2) = inputs
                if n1 == n2:
                    new_name = c.join([l1, l2])
                elif n1 + 1 == n2:
                    new_name = "VAL"
                if new_name is not None:
                    new_names[w] = n2, new_name
                    renamed = True
    new_names = {
        k: l + ("" if n is None else "_{:02d}".format(n))
        for k, (n, l) in new_names.items()
    }
    # Generate graphviz graph
    with open("/tmp/toto.dot", "w") as f:
        f.write("digraph g {\n")
        for n in sorted(new_names.values()):
            color = None
            if n.startswith("x_"):
                color = "green"
            elif n.startswith("y_"):
                color = "blue"
            elif n.startswith("z_"):
                color = "red"
            if color is not None:
                f.write(n + " [color=" + color + "]\n")
        lines = sorted(
            [
                '{} -> {} [label="{}" comment="{} {} {} -> {} ({})"]\n'.format(
                    new_names[v], new_names[w], c, w1, c, w2, w, v
                )
                for w, w1, c, w2 in gates
                for v in (w1, w2)
            ]
        )
        for l in lines:
            f.write(l)
        f.write("}\n")


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
    part2 = []
    for pair in swaps:
        part2.extend(pair)
    print(",".join(sorted(part2)) == "jqf,mdd,skh,wpd,wts,z11,z19,z37")


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
