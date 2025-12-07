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
    return string.splitlines()


def get_worksheet_from_file(file_path=top_dir + "resources/year2025_day6_input.txt"):
    with open(file_path) as f:
        return get_worksheet_from_lines(f.read())


def get_grand_total(worksheet):
    op_line = [op[o] for o in worksheet[-1] if o in op]
    int_lines = [[int(n) for n in re.split('\s+', l.strip())] for l in worksheet[:-1]]
    int_cols = [list(i) for i in zip(*int_lines)]
    return sum(op(col) for op, col in zip(op_line, int_cols))


def get_grand_total2(worksheet):
    ops = [op[o] for o in worksheet[-1] if o in op]
    nb_groups = "-".join("".join(i).strip() for i in zip(*worksheet[:-1])).split('--')
    int_cols = [[int(v) for v in s.split("-")] for s in nb_groups]
    return sum(o(col) for col, o in zip(int_cols, ops))


def run_tests():
    worksheet = get_worksheet_from_lines(
        """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """
    )
    assert get_grand_total(worksheet) == 4277556
    assert get_grand_total2(worksheet) == 3263827


def get_solutions():
    worksheet = get_worksheet_from_file()
    print(get_grand_total(worksheet) == 5733696195703)
    print(get_grand_total2(worksheet) == 10951882745757)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
