# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import collections


def get_intcode_from_string(s):
    return [int(v) for v in s.split(",")]


def get_intcode_from_file(file_path):
    with open(file_path) as f:
        for l in f:
            return get_intcode_from_string(l)


def parse_op_code(op):
    """Return op, mode1, mode2, mode3."""
    p100, de = divmod(op, 100)
    p1000, c = divmod(p100, 10)
    p10000, b = divmod(p1000, 10)
    p100000, a = divmod(p10000, 10)
    assert op == a * 10000 + b * 1000 + c * 100 + de
    return de, c, b, a


def get_value(intcode, pos, mode, relative_base):
    val = intcode[pos]
    if mode == 0:  # Position mode
        return intcode[val]
    elif mode == 1:  # Immediate mode
        return val
    elif mode == 2:  # Relative mode
        return intcode[val + relative_base]
    else:
        assert False

def set_value(intcode, pos, mode, relative_base, value):
    val = intcode[pos]
    if mode == 0:  # Position mode
        intcode[val] = value
    elif mode == 2:  # Relative mode
        intcode[val + relative_base] = value
    else:
        assert False


def get_values_from_pos(intcode, pos, modes, relative_base):
    return [
        get_value(intcode, pos + i, mode, relative_base)
        for i, mode in enumerate(modes, start=1)
    ]


def run(intcode, input_=None):
    intcode = collections.defaultdict(int, enumerate(intcode))
    output = []
    pos, relative_base = 0, 0
    while True:
        op, mode1, mode2, mode3 = parse_op_code(intcode[pos])
        if op == 99:
            final_intcode = [intcode[v] for v in range(max(intcode) + 1)]
            return final_intcode, output
        elif op == 1:  # Addition
            a, b = get_values_from_pos(intcode, pos, [mode1, mode2], relative_base)
            set_value(intcode, pos + 3, mode3, relative_base, a + b)
            pos += 4
        elif op == 2:  # Multiplication
            a, b = get_values_from_pos(intcode, pos, [mode1, mode2], relative_base)
            set_value(intcode, pos + 3, mode3, relative_base, a * b)
            pos += 4
        elif op == 3:  # Save-input
            assert input_ is not None
            set_value(intcode, pos + 1, mode1, relative_base, input_)
            pos += 2
        elif op == 4:  # Output
            a = get_value(intcode, pos + 1, mode1, relative_base)
            output.append(a)
            pos += 2
        elif op == 5:  # Jump-if-true
            a, b = get_values_from_pos(intcode, pos, [mode1, mode2], relative_base)
            pos = b if a else pos + 3
        elif op == 6:  # Jump-if-false
            a, b = get_values_from_pos(intcode, pos, [mode1, mode2], relative_base)
            pos = b if not a else pos + 3
        elif op == 7:  # Less-then
            a, b = get_values_from_pos(intcode, pos, [mode1, mode2], relative_base)
            set_value(intcode, pos + 3, mode3, relative_base, 1 if a < b else 0)
            pos += 4
        elif op == 8:  # Equals
            a, b = get_values_from_pos(intcode, pos, [mode1, mode2], relative_base)
            set_value(intcode, pos + 3, mode3, relative_base, 1 if a == b else 0)
            pos += 4
        elif op == 9:  # Relative base
            a = get_value(intcode, pos + 1, mode1, relative_base)
            relative_base += a
            pos += 2
        else:
            assert False


def run_verb_noun(intcode, noun, verb):
    """Specific to day 2 ?."""
    intcode = list(intcode)
    intcode[1] = noun
    intcode[2] = verb
    intcode, _ = run(intcode)
    return intcode[0]


def run_diagnostic(intcode, input_):
    """Specific to day 5 ?."""
    _, output = run(intcode, input_)
    diag = [v for v in output if v != 0]
    assert len(diag) == 1
    return diag[0]


def run_tests_day2():
    intcode = get_intcode_from_string("1,9,10,3,2,3,11,0,99,30,40,50")
    assert run(intcode) == ([3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50], [])
    assert run_verb_noun(intcode, 9, 10) == 3500
    intcode = get_intcode_from_string("1,0,0,0,99")
    assert run(intcode) == ([2, 0, 0, 0, 99], [])
    assert run_verb_noun(intcode, 0, 0) == 2
    intcode = get_intcode_from_string("2,3,0,3,99")
    assert run(intcode) == ([2, 3, 0, 6, 99], [])
    intcode = get_intcode_from_string("2,4,4,5,99,0")
    assert run(intcode) == ([2, 4, 4, 5, 99, 9801], [])
    intcode = get_intcode_from_string("1,1,1,4,99,5,6,0,99")
    assert run(intcode) == ([30, 1, 1, 4, 2, 5, 6, 0, 99], [])


def run_tests_day5():
    intcode = get_intcode_from_string("1002,4,3,4,33")
    assert run(intcode) == ([1002, 4, 3, 4, 99], [])
    intcode = get_intcode_from_string("1101,100,-1,4,0")
    assert run(intcode) == ([1101, 100, -1, 4, 99], [])
    intcode = get_intcode_from_string("3,9,8,9,10,9,4,9,99,-1,8")
    assert run(intcode, 8) == ([3, 9, 8, 9, 10, 9, 4, 9, 99, 1, 8], [1])
    assert run(intcode, 7) == ([3, 9, 8, 9, 10, 9, 4, 9, 99, 0, 8], [0])
    intcode = get_intcode_from_string("3,9,7,9,10,9,4,9,99,-1,8")
    assert run(intcode, 8) == ([3, 9, 7, 9, 10, 9, 4, 9, 99, 0, 8], [0])
    assert run(intcode, 7) == ([3, 9, 7, 9, 10, 9, 4, 9, 99, 1, 8], [1])
    intcode = get_intcode_from_string("3,3,1108,-1,8,3,4,3,99")
    assert run(intcode, 8) == ([3, 3, 1108, 1, 8, 3, 4, 3, 99], [1])
    assert run(intcode, 7) == ([3, 3, 1108, 0, 8, 3, 4, 3, 99], [0])
    intcode = get_intcode_from_string("3,3,1107,-1,8,3,4,3,99")
    assert run(intcode, 8) == ([3, 3, 1107, 0, 8, 3, 4, 3, 99], [0])
    assert run(intcode, 7) == ([3, 3, 1107, 1, 8, 3, 4, 3, 99], [1])
    intcode = get_intcode_from_string("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9")
    assert run(intcode, 0) == (
        [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, 0, 0, 1, 9],
        [0],
    )
    assert run(intcode, 1) == (
        [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, 1, 1, 1, 9],
        [1],
    )
    intcode = get_intcode_from_string("3,3,1105,-1,9,1101,0,0,12,4,12,99,1")
    assert run(intcode, 0) == ([3, 3, 1105, 0, 9, 1101, 0, 0, 12, 4, 12, 99, 0], [0])
    assert run(intcode, 1) == ([3, 3, 1105, 1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], [1])
    intcode = get_intcode_from_string(
        "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
    )
    assert run(intcode, 7)[1] == [999]
    assert run(intcode, 8)[1] == [1000]
    assert run(intcode, 9)[1] == [1001]


def run_tests_day9():
    intcode = get_intcode_from_string(
        "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
    )
    assert run(intcode)[1] == intcode
    intcode = get_intcode_from_string("1102,34915192,34915192,7,4,7,99,0")
    assert run(intcode)[1] == [1219070632396864]
    intcode = get_intcode_from_string("104,1125899906842624,99")
    assert run(intcode)[1] == [1125899906842624]
    # More tests from Reddit: https://www.reddit.com/r/adventofcode/comments/e8aw9j/comment/fac3294/?utm_source=share&utm_medium=web2x&context=3
    intcode = get_intcode_from_string("109,-1,4,1,99")
    assert run(intcode)[1] == [-1]
    intcode = get_intcode_from_string("109,-1,104,1,99")
    assert run(intcode)[1] == [1]
    intcode = get_intcode_from_string("109,-1,204,1,99")
    assert run(intcode)[1] == [109]
    intcode = get_intcode_from_string("109,1,9,2,204,-6,99")
    assert run(intcode)[1] == [204]
    intcode = get_intcode_from_string("109,1,109,9,204,-6,99")
    assert run(intcode)[1] == [204]
    intcode = get_intcode_from_string("109,1,209,-1,204,-106,99")
    assert run(intcode)[1] == [204]
    intcode = get_intcode_from_string("109,1,3,3,204,2,99")
    assert run(intcode, 42)[1] == [42]
    assert run(intcode, 314)[1] == [314]
    intcode = get_intcode_from_string("109,1,203,2,204,2,99")
    assert run(intcode, 42)[1] == [42]
    assert run(intcode, 314)[1] == [314]


def run_tests():
    run_tests_day2()
    run_tests_day5()
    run_tests_day9()


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    end = datetime.datetime.now()
    print(end - begin)
