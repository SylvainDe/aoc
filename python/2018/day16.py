# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_registers_from_string(string):
    return tuple(int(s) for s in string.split("[")[1][:-1].split(", "))

def get_instructions_from_string(string):
    return tuple(int(s) for s in string.split())

def get_sample_from_string(string):
    before, instr, after = string.splitlines()
    return get_registers_from_string(before), \
        get_registers_from_string(after), \
        get_instructions_from_string(instr)


def get_inputs_from_lines(string):
    samples, prgm = string.split("\n\n\n\n")
    samples = [get_sample_from_string(s) for s in samples.split("\n\n")]
    prgm = [get_instructions_from_string(s) for s in prgm.splitlines()]
    return samples, prgm


def get_inputs_from_file(file_path=top_dir + "resources/year2018_day16_input.txt"):
    with open(file_path) as f:
        return get_inputs_from_lines(f.read())

opcodes = ["addr", "addi", "mulr", "muli", "banr", "bani", "borr", "bori", "setr", "seti", "gtir", "gtri", "gtrr", "eqir", "eqri", "eqrr"]

def apply_ins(op, a, b, c, register):
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

def get_possible_opcodes(sample):
    before, after, instr = sample
    return set(op for op in opcodes if tuple(apply_ins(op, *instr[1:], list(before))) == after)


def get_nb_of_possible_opcodes(sample):
    return len(get_possible_opcodes(sample))


def find_opcodes(samples):
    candidates = {
        n: set(opcodes) for n in range(len(opcodes))
    }
    for s in samples:
        _, _, instr = s
        opcode = instr[0]
        candidates[opcode] = candidates[opcode] & get_possible_opcodes(s)
    update = True
    while update:
        update = False
        known_codes = {code: next(iter(cands)) for code, cands in candidates.items() if len(cands) == 1}
        for code, cands in candidates.items():
            new_cands = set(cands)
            for opcode2, code2 in known_codes.items():
                if opcode2 == code:
                    assert new_cands == set([code2])
                else:
                    new_cands.discard(code2)
            if new_cands != cands:
                candidates[code] = new_cands
                update = True
    known_codes = {code: next(iter(cands)) for code, cands in candidates.items() if len(cands) == 1}
    assert len(known_codes) == len(candidates)
    return known_codes


def run_program(prgm, known_codes):
    register = [0, 0, 0, 0]
    for ins in prgm:
        op, a, b, c = ins
        apply_ins(known_codes[op], a, b, c, register)
    return register

def run_tests():
    sample = """Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]"""
    sample = get_sample_from_string(sample)
    assert get_nb_of_possible_opcodes(sample) == 3

def get_solutions():
    inputs = get_inputs_from_file()
    samples, prgm = inputs
    print(sum(get_nb_of_possible_opcodes(s) >= 3 for s in samples) == 636)
    known_codes = find_opcodes(samples)
    print(run_program(prgm, known_codes)[0] == 674)

if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
