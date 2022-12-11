# vi: set shiftwidth=4 tabstop=4 expandtab:
import collections
import datetime
import re
import operator

operations = {
    "*": operator.mul,
    "+": operator.add,
    "-": operator.sub,
}

def get_operation_from_string(string):
    left, op, right = string.split(" ")
    return lambda old: operations[op](
        old if left == "old" else int(left),
        old if right == "old" else int(right)
    )

MonkeyInput = collections.namedtuple("MonkeyInput", ("id", "start_items", "operation", "div", "if_true", "if_false"))


# "'Monkey 0:\n  Starting items: 79, 98\n  Operation: new = old * 19\n  Test: divisible by 23\n    If true: throw to monkey 2\n    If false: throw to monkey 3'"
monkey_re = re.compile(r"^Monkey (\d+):\n  Starting items: (.*)\n  Operation: new = (.*)\n  Test: divisible by (\d+)\n    If true: throw to monkey (\d+)\n    If false: throw to monkey (\d+)$")


def get_monkey_from_string(string):
    m_id, items, operation, div_test, if_true, if_false = monkey_re.match(string).groups()
    m_id, div_test, if_true, if_false = (int(s) for s in (m_id, div_test, if_true, if_false))
    items = tuple(int(c) for c in items.split(", "))
    operation = get_operation_from_string(operation)
    return MonkeyInput(m_id, items, operation, div_test, if_true, if_false)

def get_monkeys_from_lines(string):
    return [get_monkey_from_string(l) for l in string.split("\n\n")]

def get_monkey_from_file(file_path="../../resources/year2022_day11_input.txt"):
    with open(file_path) as f:
        return get_monkeys_from_lines(f.read())


def run_tests():
    monkeys = get_monkeys_from_lines("""Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1""")
    print(monkeys)

def get_solutions():
    monkeys = get_monkey_from_file()
    print(monkeys)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
