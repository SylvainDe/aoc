# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_numbers_from_lines(string):
    return [int(l) for l in string.splitlines()]

def get_numbers_from_file(file_path="../../resources/year2022_day20_input.txt"):
    with open(file_path) as f:
        return get_numbers_from_lines(f.read())

def move(src, shift, lst):
    mod = len(lst) -1
    dst = ((src + shift - 1) % mod) + 1
    val = lst.pop(src)
    lst.insert(dst, val)
    return lst # Only to make testing easier

def mix(numbers):
    # Add index to numbers for tracking
    indexed_numbers = list(enumerate(numbers))
    mixed_numbers = list(indexed_numbers)
    assert id(indexed_numbers) != id(mixed_numbers)
    for val in indexed_numbers:
        src = mixed_numbers.index(val)
        move(src, val[1], mixed_numbers)
    mixed_numbers = [v[1] for v in mixed_numbers]
    idx = mixed_numbers.index(0)
    l = len(numbers)
    return sum(mixed_numbers[(i+idx)%l] for i in (1000, 2000, 3000))

def run_tests():
    # Small tests
    lst = [4, 5, 6, 1, 7, 8, 9]
    val = 1
    assert move(lst.index(val), val, lst) == [4, 5, 6, 7, 1, 8, 9]
    lst = [4, -2, 5, 6, 7, 8, 9]
    val = -2
    assert move(lst.index(val), val, lst) == [4, 5, 6, 7, 8, -2, 9]
    # Big test
    lst1 = [1, 2, -3, 3, -2, 0, 4]
    lst2 = [2, 1, -3, 3, -2, 0, 4]
    lst3 = [1, -3, 2, 3, -2, 0, 4]
    lst4 = [1, 2, 3, -2, -3, 0, 4]
    lst5 = [1, 2, -2, -3, 0, 3, 4]
    lst6 = [1, 2, -3, 0, 3, 4, -2]
    lst7 = [1, 2, -3, 0, 3, 4, -2]
    lst8 = [1, 2, -3, 4, 0, 3, -2]
    val = 1
    assert move(lst1.index(val), val, lst1) == lst2
    val = 2
    assert move(lst2.index(val), val, lst2) == lst3
    val = -3
    assert move(lst3.index(val), val, lst3) == lst4
    val = 3
    assert move(lst4.index(val), val, lst4) == lst5
    val = -2
    assert move(lst5.index(val), val, lst5) == lst6
    val = 0
    assert move(lst6.index(val), val, lst6) == lst7
    val = 4
    assert move(lst7.index(val), val, lst7) == lst8
    numbers = get_numbers_from_lines("""1
2
-3
3
-2
0
4""")
    assert mix(numbers) == 3

def get_solutions():
    numbers = get_numbers_from_file()
    print(mix(numbers) == 3466)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
