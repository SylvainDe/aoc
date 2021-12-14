# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import collections


def get_instructions_from_file(file_path="day1_input.txt"):
    with open(file_path) as f:
        for l in f:
            return l.strip()


def get_final_floor(instructions):
    c = collections.Counter(instructions)
    return c["("] - c[")"]


def run_tests():
    assert get_final_floor("(())") == 0
    assert get_final_floor("()()") == 0
    assert get_final_floor("(((") == 3
    assert get_final_floor("())") == -1


def get_solutions():
    instructions = get_instructions_from_file()
    print(get_final_floor(instructions))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
