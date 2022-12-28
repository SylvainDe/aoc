# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import operator
import collections

operations = {
    "*": operator.mul,
    "+": operator.add,
    "-": operator.sub,
    "/": operator.floordiv,
}

inverses = {
    # A + B = x is also A = x - B or B = x - A
    operator.add: lambda left, right, expr: (
        (expr, operator.sub, right),
        (expr, operator.sub, left),
    ),
    # A // B = x is also A = x * B or B = A // x
    operator.floordiv: lambda left, right, expr: (
        (expr, operator.mul, right),
        (left, operator.floordiv, expr),
    ),
    # A - B = x is also A = x + B or B = A - x
    operator.sub: lambda left, right, expr: (
        (expr, operator.add, right),
        (left, operator.sub, expr),
    ),
    # A * B = x is also A = x // B or B = x // A
    operator.mul: lambda left, right, expr: (
        (expr, operator.floordiv, right),
        (expr, operator.floordiv, left),
    ),
}


def get_monkey_from_line(string):
    sep = ": "
    name, mid, expr = string.partition(sep)
    assert mid == sep
    expr = expr.split(" ")
    expr = int(expr[0]) if len(expr) == 1 else (expr[0], operations[expr[1]], expr[2])
    return name, expr


def get_monkeys_from_lines(string):
    return [get_monkey_from_line(l) for l in string.splitlines()]


def get_monkeys_from_file(file_path="../../resources/year2022_day21_input.txt"):
    with open(file_path) as f:
        return get_monkeys_from_lines(f.read())


def eval_expr(expr, values):
    if type(expr) == int:
        return expr
    left, func, right = expr
    if type(left) != int:
        left = values.get(left)
    if left is None:
        return None
    if type(right) != int:
        right = values.get(right)
    if right is None:
        return None
    return func(left, right)


def get_values(monkey_lst):
    monkey_dict = dict()
    deps = collections.defaultdict(set)
    for name, expr in monkey_lst:
        monkey_dict.setdefault(name, []).append(expr)
        if type(expr) != int:
            left, _, right = expr
            deps[left].add(name)
            deps[right].add(name)
    values = dict()
    queue = collections.deque(monkey_dict.keys())
    while queue:
        name = queue.popleft()
        if name in values:
            continue
        for expr in monkey_dict[name]:
            expr_value = eval_expr(expr, values)
            if expr_value is not None:
                values[name] = expr_value
                queue.extend(deps[name])
                break
    return values


def get_root_value(monkeys):
    return get_values(monkeys)["root"]


def get_hmn_value(monkeys):
    lst = []
    # Tweak content of list to convey all the relationships between values
    for name, expr in monkeys:
        if name == "humn":
            continue
        elif type(expr) == int:
            lst.append((name, expr))
        else:
            left, func, right = expr
            # Express the relation in different ways
            if name == "root":
                expr = 0
                new_left, new_right = (right, operator.add, name), (
                    left,
                    operator.add,
                    name,
                )
            else:
                new_left, new_right = inverses[func](left, right, name)
            lst.append((left, new_left))
            lst.append((right, new_right))
            lst.append((name, expr))
    return get_values(lst)["humn"]


def run_tests():
    monkeys = get_monkeys_from_lines(
        """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""
    )
    assert get_root_value(monkeys) == 152
    assert get_hmn_value(monkeys) == 301


def get_solutions():
    monkeys = get_monkeys_from_file()
    print(get_root_value(monkeys) == 353837700405464)
    print(get_hmn_value(monkeys) == 3678125408017)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
