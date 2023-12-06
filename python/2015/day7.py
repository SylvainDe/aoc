# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import operator

max_val = 65535

binary_ops = {
    " AND ": operator.and_,
    " OR ": operator.or_,
    " LSHIFT ": operator.lshift,
    " RSHIFT ": operator.rshift,
}

unary_ops = {"NOT ": lambda x: max_val - x}


def get_parse_expr(expr):
    for bin_name, bin_func in binary_ops.items():
        left, mid, right = expr.partition(bin_name)
        if mid == bin_name:
            return (bin_func, left, right)
    for un_name, un_func in unary_ops.items():
        if expr.startswith(un_name):
            return (un_func, expr[len(un_name) :])
    return (expr,)


def get_wire_from_string(s, sep=" -> "):
    expr, mid, wire = s.partition(sep)
    assert mid == sep
    return wire, get_parse_expr(expr)


def get_wires_from_file(file_path="../../resources/year2015_day7_input.txt"):
    with open(file_path) as f:
        return dict(get_wire_from_string(l.strip()) for l in f)


def eval_wire(wire, wires):
    return eval_wire_(wire, dict(), wires)


def eval_wire_(wire, env, wires):
    val = env.get(wire, None)
    if val is not None:
        return val
    expr = wires.get(wire, None)
    if expr is None:
        ret = int(wire)
    elif len(expr) == 3:
        func, left, right = expr
        ret = func(eval_wire_(left, env, wires), eval_wire_(right, env, wires))
    elif len(expr) == 2:
        func, value = expr
        ret = func(eval_wire_(value, env, wires))
    else:
        value = expr[0]
        ret = eval_wire_(value, env, wires)
    env[wire] = ret
    return ret


def run_tests():
    wires = [
        "123 -> x",
        "456 -> y",
        "x AND y -> d",
        "x OR y -> e",
        "x LSHIFT 2 -> f",
        "y RSHIFT 2 -> g",
        "NOT x -> h",
        "NOT y -> i",
    ]
    wires = dict(get_wire_from_string(l) for l in wires)
    values = {
        "d": 72,
        "e": 507,
        "f": 492,
        "g": 114,
        "h": 65412,
        "i": 65079,
        "x": 123,
        "y": 456,
    }
    for name, value in values.items():
        assert eval_wire(name, wires) == value


def get_solutions():
    wires = get_wires_from_file()
    val_a = eval_wire("a", wires)
    print(val_a == 16076)
    wires["b"] = str(val_a)
    val_a2 = eval_wire("a", wires)
    print(val_a2 == 2797)  # Happens to be wrong ?!


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
