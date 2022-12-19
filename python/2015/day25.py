# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import re

# To continue, please consult the code grid in the manual.  Enter the code at row 123, column 45.
code_re = re.compile(r"^To continue, please consult the code grid in the manual.  Enter the code at row (\d+), column (\d+).$")

def get_pos_from_line(string):
    return tuple(int(s) for s in code_re.match(string).groups())

def get_pos_from_file(file_path="../../resources/year2015_day25_input.txt"):
    with open(file_path) as f:
        for l in f:
            return get_pos_from_line(l.strip())

def get_index(pos):
    row, col = pos
    n = row + col - 2
    return col + n*(n+1) // 2

def get_code_at_index(n, start=20151125, mult=252533, mod=33554393):
    return (start * pow(mult, n-1, mod)) % mod

def get_code(pos):
    return get_code_at_index(get_index(pos))

def run_tests():
    assert get_index((4, 2)) == 12
    assert get_index((1, 5)) == 15
    res1 = 20151125
    res2 = 31916031
    res3 = 18749137
    res20 = 15514188
    assert get_code_at_index(1) == res1
    assert get_code((1, 1)) == res1
    assert get_code_at_index(2) == res2
    assert get_code((2, 1)) == res2
    assert get_code_at_index(3) == res3
    assert get_code((1, 2)) == res3
    assert get_code_at_index(20) == res20
    assert get_code((2, 5)) == res20

def get_solutions():
    print(get_code(get_pos_from_file()) == 2650453)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
