# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import itertools

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_register_from_line(string):
    beg, mid, end = string.partition(": ")
    return beg[-1], int(end)


def get_computer_from_lines(string):
    registers, mid, program = string.partition("\n\n")
    assert mid == "\n\n"
    _, _, program = program.partition(": ")
    registers = dict(get_register_from_line(l) for l in registers.splitlines())
    program = [int(v) for v in program.split(",")]
    return registers, program


def get_computer_from_file(file_path=top_dir + "resources/year2024_day17_input.txt"):
    with open(file_path) as f:
        return get_computer_from_lines(f.read())


def get_combo_operand(operand, registers):
    register_mapping = {
        4: "A",
        5: "B",
        6: "C",
    }
    val_reg = register_mapping.get(operand, None)
    if val_reg is not None:
        return registers[val_reg]
    assert 0 <= operand <= 3
    return operand


def run_computer(computer):
    registers, program = computer
    registers = dict(registers)
    pointer = 0
    output = []
    while True:
        try:
            opcode, operand = program[pointer], program[pointer + 1]
        except IndexError:
            break
        pointer += 2
        if opcode == 0:
            registers["A"] = registers["A"] // (
                2 ** get_combo_operand(operand, registers)
            )
        elif opcode == 1:
            registers["B"] = registers["B"] ^ operand
        elif opcode == 2:
            registers["B"] = get_combo_operand(operand, registers) % 8
        elif opcode == 3:
            if registers["A"]:
                pointer = operand
        elif opcode == 4:
            registers["B"] = registers["B"] ^ registers["C"]
        elif opcode == 5:
            output.append(get_combo_operand(operand, registers) % 8)
        elif opcode == 6:
            registers["B"] = registers["A"] // (
                2 ** get_combo_operand(operand, registers)
            )
        elif opcode == 7:
            registers["C"] = registers["A"] // (
                2 ** get_combo_operand(operand, registers)
            )
        else:
            assert False
    return output
    return ",".join(str(o) for o in output)


def find_a_for_copy(computer):
    registers, program = computer
    for a in itertools.count():
        registers["A"] = a
        if run_computer((registers, program)) == program:
            return a


def run_tests():
    computer = get_computer_from_lines(
        """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""
    )
    assert ",".join(str(o) for o in run_computer(computer)) == "4,6,3,5,6,3,5,2,1,0"
    computer = get_computer_from_lines(
        """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""
    )
    assert find_a_for_copy(computer) == 117440


def get_solutions():
    computer = get_computer_from_file()
    print(",".join(str(o) for o in run_computer(computer)) == "7,5,4,3,4,5,3,4,6")
    print(find_a_for_copy(computer))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
