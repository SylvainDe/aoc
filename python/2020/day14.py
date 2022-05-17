# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import re
import itertools


def get_program_from_file(file_path="../../resources/year2020_day14_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]


# mask = X100110110X011000101000101XX11001X11
mask_re = re.compile(r"^mask = (?P<mask>[01X]+)$")
# mem[5201] = 1838761
mem_re = re.compile(r"^mem\[(?P<addr>\d+)\] = (?P<value>\d+)")


def apply_mask(value, mask):
    value = format(value, "0%db" % len(mask))
    bits = [bv if bm == "X" else bm for bv, bm in zip(value, mask)]
    return int("".join(bits), 2)


def all_combinations(lst):
    for l in range(len(lst) + 1):
        for comb in itertools.combinations(lst, l):
            yield comb


def apply_mask2(value, mask):
    value = format(value, "0%db" % len(mask))
    floating = []
    base_val = 0
    for i, (bval, bmask) in enumerate(reversed(list(zip(value, mask)))):
        val = 2 ** i
        if bmask == "X":
            floating.append(val)
        elif int(bmask) or int(bval):
            base_val += val
    return [base_val + sum(comb) for comb in all_combinations(floating)]


def run_program(program):
    mask = ""
    memory = dict()
    for line in program:
        m_mask = mask_re.fullmatch(line)
        if m_mask is not None:
            d = m_mask.groupdict()
            mask = d["mask"]
        else:
            m_mem = mem_re.fullmatch(line)
            if m_mem is not None:
                d = m_mem.groupdict()
                memory[int(d["addr"])] = apply_mask(int(d["value"]), mask)
            else:
                raise ValueError(line)
    return sum(v for v in memory.values())


def run_program2(program):
    mask = ""
    memory = dict()
    for line in program:
        m_mask = mask_re.fullmatch(line)
        if m_mask is not None:
            d = m_mask.groupdict()
            mask = d["mask"]
        else:
            m_mem = mem_re.fullmatch(line)
            if m_mem is not None:
                d = m_mem.groupdict()
                v = int(d["value"])
                for addr in apply_mask2(int(d["addr"]), mask):
                    memory[addr] = v
            else:
                raise ValueError(line)
    return sum(v for v in memory.values())


def run_tests():
    example1 = [
        "mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X",
        "mem[8] = 11",
        "mem[7] = 101",
        "mem[8] = 0",
    ]
    assert apply_mask(11, "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X") == 73
    assert apply_mask(101, "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X") == 101
    assert apply_mask(0, "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X") == 64
    assert run_program(example1) == 165
    example2 = [
        "mask = 000000000000000000000000000000X1001X",
        "mem[42] = 100",
        "mask = 00000000000000000000000000000000X0XX",
        "mem[26] = 1",
    ]
    assert sorted(apply_mask2(42, "000000000000000000000000000000X1001X")) == [
        26,
        27,
        58,
        59,
    ]
    assert sorted(apply_mask2(26, "00000000000000000000000000000000X0XX")) == [
        16,
        17,
        18,
        19,
        24,
        25,
        26,
        27,
    ]
    assert run_program2(example2) == 208


def get_solutions():
    program = get_program_from_file()
    print(run_program(program) == 6559449933360)
    print(run_program2(program) == 3369767240513)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
