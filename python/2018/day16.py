# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_registers_from_string(string):
    return tuple(int(s) for s in string.split("[")[1][:-1].split(", "))


def get_sample_from_string(string):
    before, instr, after = string.splitlines()
    return get_registers_from_string(before), \
        get_registers_from_string(after), \
        tuple(int(s) for s in instr.split())


def get_inputs_from_lines(string):
    samples, prgm = string.split("\n\n\n")
    samples = [get_sample_from_string(s) for s in samples.split("\n\n")]
    return samples, prgm


def get_inputs_from_file(file_path=top_dir + "resources/year2018_day16_input.txt"):
    with open(file_path) as f:
        return get_inputs_from_lines(f.read())

opcodes = ["addr", "addi", "mulr", "muli", "banr", "bani", "borr", "bori", "setr", "seti", "gtir", "gtri", "gtrr", "eqir", "eqri", "eqrr"]

def apply_opcode(op, instruction, register):
    register = list(register)
    a, b, c = instruction
    if op == "addr":
        register[c] = register[a] + register[b]
    elif op == "addi":
        register[c] = register[a] + b
    elif op == "mulr":
        register[c] = register[a] * register[b]
    elif op == "muli":
        register[c] = register[a] * b
    elif op == "banr":
        register[c] = register[a] & register[b]
    elif op == "bani":
        register[c] = register[a] & b
    elif op == "borr":
        register[c] = register[a] | register[b]
    elif op == "bori":
        register[c] = register[a] | b
    elif op == "setr":
        register[c] = register[a]
    elif op == "seti":
        register[c] = a
    elif op == "gtir":
        register[c] = a > register[b]
    elif op == "gtri":
        register[c] = register[a] > b
    elif op == "gtrr":
        register[c] = register[a] > register[b]
    elif op == "eqir":
        register[c] = a == register[b]
    elif op == "eqri":
        register[c] = register[a] == b
    elif op == "eqrr":
        register[c] = register[a] == register[b]
    else:
        assert False
    return register


def get_nb_of_possible_opcodes(sample):
    before, after, instr = sample
    return sum(tuple(apply_opcode(op, instr[1:], before)) == after for op in opcodes)

def run_tests():
    sample = """Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]"""
    sample = get_sample_from_string(sample)
    assert get_nb_of_possible_opcodes(sample) == 3

def get_solutions():
    inputs = get_inputs_from_file()
    samples, prgm = inputs
    print(sum(get_nb_of_possible_opcodes(s) >= 3 for s in samples))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
