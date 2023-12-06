# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import collections
import operator


resource_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../resources/"

operators = {
    "==": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    "<": operator.lt,
    ">=": operator.ge,
    "<=": operator.le,
}

coeff = {
    "inc": 1,
    "dec": -1,
}


def get_instruction_from_line(s):
    reg, direction, amount, if_, reg2, op, value = s.split()
    assert if_ == "if"
    return (reg, direction, int(amount), reg2, operators[op], int(value))


def get_instructions_from_string(s):
    return [get_instruction_from_line(l) for l in s.splitlines()]


def get_instructions_from_file(file_path=resource_dir + "year2017_day8_input.txt"):
    with open(file_path) as f:
        return get_instructions_from_string(f.read())


def get_max_register(instructions):
    maximums = []
    registers = collections.defaultdict(int)
    for instruction in instructions:
        reg, direction, amount, reg2, op, value = instruction
        if op(registers[reg2], value):
            registers[reg] += amount * coeff[direction]
            maximums.append(max(registers.values()))
    return maximums[-1], max(maximums)


def run_tests():
    instructions = get_instructions_from_string(
        """b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10"""
    )
    assert get_max_register(instructions) == (1, 10)


def get_solutions():
    instructions = get_instructions_from_file()
    max1, max2 = get_max_register(instructions)
    print(max1 == 7787)
    print(max2 == 8997)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
