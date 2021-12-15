# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_string_from_file(file_path="day10_input.txt"):
    with open(file_path) as f:
        for l in f:
            return [int(d) for d in l.strip()]


def look_and_say(seq):
    last = None
    ret = []
    for d in seq:
        if d == last:
            count += 1
        else:
            if last is not None:
                ret.extend([count, last])
            last, count = d, 1
    if last is not None:
        ret.extend([count, last])
    return ret


def repeated_look_and_say(seq, n):
    for i in range(n):
        seq = look_and_say(seq)
    return seq


def run_tests():
    seq = [1]
    assert repeated_look_and_say(seq, 0) == [1]
    assert repeated_look_and_say(seq, 1) == [1, 1]
    assert repeated_look_and_say(seq, 2) == [2, 1]
    assert repeated_look_and_say(seq, 3) == [1, 2, 1, 1]
    assert repeated_look_and_say(seq, 4) == [1, 1, 1, 2, 2, 1]
    assert repeated_look_and_say(seq, 5) == [3, 1, 2, 2, 1, 1]


def get_solutions():
    seq = get_string_from_file()
    print(len(repeated_look_and_say(seq, 40)))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
