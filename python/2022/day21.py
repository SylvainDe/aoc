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

def get_root_value(monkeys):
    monkey_dict = { name: expr for name, expr in monkeys }
    deps = dict()
    for name, expr in monkey_dict.items():
        if type(expr) != int:
            deps.setdefault(expr[0], []).append(name)
            deps.setdefault(expr[2], []).append(name)
    values = dict()
    queue = collections.deque(monkey_dict.keys())
    while queue:
        name = queue.popleft()
        if name in values:
            continue
        expr = monkey_dict[name]
        expr_value = None
        if type(expr) == int:
            expr_value = expr
        else:
            left, func, right = expr
            left, right = values.get(left) , values.get(right)
            if left is not None and right is not None:
                expr_value = func(left, right)
        if expr_value is not None:
            values[name] = expr_value
            queue.extend(deps.get(name, []))
    return values["root"]


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

def get_solutions():
    monkeys = get_monkeys_from_file()
    print(get_root_value(monkeys))

if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
