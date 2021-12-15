# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_wire_from_string(s, sep=" -> "):
    expr, mid, wire = s.partition(sep)
    assert mid == sep
    return wire, expr


def get_wires_from_file(file_path="day7_input.txt"):
    with open(file_path) as f:
        return dict(get_wire_from_string(l.strip()) for l in f)


max_val = 65535

binary_ops = {
    " AND ": lambda x, y: x & y,
    " OR ": lambda x, y: x | y,
    " LSHIFT ": lambda x, y: x << y,
    " RSHIFT ": lambda x, y: x >> y,
}

unary_ops = {"NOT ": lambda x: max_val - x}


def eval_wire(wire, wires):
    return eval(wire, dict(), wires)


def add_val_to_env(wire, value, env):
    env[wire] = value
    return value


def eval(wire, env, wires):
    val = env.get(wire, None)
    if val is not None:
        return val
    expr = wires.get(wire, None)
    if expr is None:
        return add_val_to_env(wire, int(wire), env)
    for bin_name, bin_func in binary_ops.items():
        left, mid, right = expr.partition(bin_name)
        if mid == bin_name:
            ret = bin_func(eval(left, env, wires), eval(right, env, wires))
            return add_val_to_env(wire, ret, env)
    for un_name, un_func in unary_ops.items():
        if expr.startswith(un_name):
            remaining = expr[len(un_name) :]
            ret = un_func(eval(remaining, env, wires))
            return add_val_to_env(wire, ret, env)
    ret = eval(expr, env, wires)
    return add_val_to_env(wire, ret, env)


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
    print(eval_wire("a", wires))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
