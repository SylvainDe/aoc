# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import operator
import collections

operations = {
    "*": operator.mul,
    "+": operator.add,
    "-": operator.sub,
    "/": operator.floordiv,
    "=": operator.mul,
}

def get_monkey_from_line(string):
    sep = ": "
    name, mid, expr = string.partition(sep)
    assert mid == sep
    expr = expr.split(" ")
    if len(expr) == 1:
        expr = int(expr[0])
    else:
        expr = (expr[0], operations[expr[1]], expr[2])
    return name, expr

def get_monkeys_from_lines(string):
    return [get_monkey_from_line(l) for l in string.splitlines()]

def get_monkeys_from_file(file_path="../../resources/year2022_day21_input.txt"):
    with open(file_path) as f:
        return get_monkeys_from_lines(f.read())

def get_values(monkey_dict):
    deps = dict()
    for name, exprs in monkey_dict.items():
        for expr in exprs:
            if type(expr) != int:
                deps.setdefault(expr[0], []).append(name)
                deps.setdefault(expr[2], []).append(name)
    values = dict()
    queue = collections.deque(monkey_dict.keys())
    while queue:
        name = queue.popleft()
        if name in values:
            continue
        exprs = monkey_dict[name]
        expr_value = None
        for expr in exprs:
            if type(expr) == int:
                expr_value = expr
            else:
                left, func, right = expr
                if type(left) != int:
                    left = values.get(left)
                if type(right) != int:
                    right = values.get(right)
                if left is not None and right is not None:
                    expr_value = func(left, right)
            if expr_value is not None:
                break
        if expr_value is not None:
            values[name] = expr_value
            queue.extend(deps.get(name, []))
            # If name was expressed in different way, let's add the corresponding expressions
            for expr2 in exprs:
                if expr2 != expr:
                    left2, func2, right2 = expr2
                    if func2 == operator.eq:
                        assert expr_value == 1  # We would not learn much from an inequality
                        monkey_dict.setdefault(left2, []).append((right2, operator.add, 0))
                        monkey_dict.setdefault(right2, []).append((left2, operator.add, 0))
                    elif func2 == operator.add:
                        monkey_dict.setdefault(left2, []).append((expr_value, operator.sub, right2))
                        monkey_dict.setdefault(right2, []).append((expr_value, operator.sub, left2))
                    elif func2 == operator.floordiv:
                        monkey_dict.setdefault(left2, []).append((expr_value, operator.mul, right2))
                        monkey_dict.setdefault(right2, []).append((left2, operator.floordiv, expr_value))
                    elif func2 == operator.sub:
                        monkey_dict.setdefault(left2, []).append((expr_value, operator.add, right2))
                        monkey_dict.setdefault(right2, []).append((left2, operator.sub, expr_value))
                    elif func2 == operator.mul:
                        monkey_dict.setdefault(left2, []).append((expr_value, operator.floordiv, right2))
                        monkey_dict.setdefault(right2, []).append((expr_value, operator.floordiv, left2))
                    else:
                        print(func2)
                        assert False
                    queue.extend((left2, right2))
                    deps.setdefault(right2, []).append(left2)
                    deps.setdefault(left2, []).append(right2)
    return values

def get_root_value(monkeys):
    monkey_dict = { name: [expr] for name, expr in monkeys }
    return get_values(monkey_dict)["root"]


def get_hmn_value(monkeys):
    monkey_dict = { name: [expr] for name, expr in monkeys }
    monkey_dict.pop("humn")
    left, _, right = monkey_dict.pop("root")[0]
    monkey_dict["root"] = [1, (left, operator.eq, right)]
    return get_values(monkey_dict)["humn"]


def run_tests():
    monkeys = get_monkeys_from_lines("""root: pppw + sjmn
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
hmdt: 32""")
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
