# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import re
import operator
import math

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


op = {
    '*': math.prod,
    '+': sum,
}

def get_worksheet_from_lines(string):
    lines = [re.split('\s+', l.strip()) for l in string.splitlines()]
    int_lines = [[int(n) for n in l] for l in lines[:-1]]
    op_line = [op[o] for o in lines[-1]]
    return int_lines, op_line


def get_worksheet_from_file(file_path=top_dir + "resources/year2025_day6_input.txt"):
    with open(file_path) as f:
        return get_worksheet_from_lines(f.read())


def get_grand_total(worksheet):
    int_lines, op_line = worksheet
    int_cols = [list(i) for i in zip(*int_lines)]
    return sum(op(col) for op, col in zip(op_line, int_cols))


def get_grand_total2(worksheet):
    int_lines, op_line = worksheet
    int_cols = [list(i) for i in zip(*int_lines)]


def run_tests():
    worksheet = get_worksheet_from_lines(
        """123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +  """
    )
    assert get_grand_total(worksheet) == 4277556
    print(get_grand_total2(worksheet))


def get_solutions():
    worksheet = get_worksheet_from_file()
    print(get_grand_total(worksheet) == 5733696195703)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
