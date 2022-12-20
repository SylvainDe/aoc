# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_numbers_from_lines(string):
    return [int(l) for l in string.splitlines()]

def get_numbers_from_file(file_path="../../resources/year2022_day20_input.txt"):
    with open(file_path) as f:
        return get_numbers_from_lines(f.read())

def move(src, shift, lst):
    if shift:
        mod = len(lst) - 1
        dst = ((src + shift - 1) % mod) + 1
        val = lst.pop(src)
        lst.insert(dst, val)

def mix(numbers, nb_mix):
    # Add index to numbers for tracking
    indexed_numbers = list(enumerate(numbers))
    mixed_numbers = list(indexed_numbers)
    assert id(indexed_numbers) != id(mixed_numbers)
    for val in indexed_numbers * nb_mix:
        move(mixed_numbers.index(val), val[1], mixed_numbers)
    return [v[1] for v in mixed_numbers]

def groove(numbers):
    idx = numbers.index(0)
    l = len(numbers)
    return sum(numbers[(i+idx)%l] for i in (1000, 2000, 3000))

def mix1(numbers):
    return groove(mix(numbers, 1))

def mix2(numbers, key=811589153):
    return groove(mix([n * key for n in numbers], 10))


def run_tests():
    # Part 1: Small tests
    lst = [4, 5, 6, 1, 7, 8, 9]
    val = 1
    move(lst.index(val), val, lst)
    assert lst == [4, 5, 6, 7, 1, 8, 9]
    lst = [4, -2, 5, 6, 7, 8, 9]
    val = -2
    move(lst.index(val), val, lst)
    assert lst == [4, 5, 6, 7, 8, -2, 9]
    # Part 1: Big test step by step
    steps = [
        [1, 2, -3, 3, -2, 0, 4],
        [2, 1, -3, 3, -2, 0, 4],
        [1, -3, 2, 3, -2, 0, 4],
        [1, 2, 3, -2, -3, 0, 4],
        [1, 2, -2, -3, 0, 3, 4],
        [1, 2, -3, 0, 3, 4, -2],
        [1, 2, -3, 0, 3, 4, -2],
        [1, 2, -3, 4, 0, 3, -2],
    ]
    initial = steps[0]
    for i, val in enumerate(initial):
        l = list(steps[i])
        move(l.index(val), val, l)
        assert l == steps[i+1]
    assert mix(initial, 1) == steps[-1]
    # Part 1: Whole test
    numbers = get_numbers_from_lines("""1
2
-3
3
-2
0
4""")
    assert mix1(numbers) == 3
    # Part 2: Big test step by step
    lst1 = [811589153, 1623178306, -2434767459, 2434767459, -1623178306, 0, 3246356612]
    assert mix(lst1, 1) == [0, -2434767459, 3246356612, -1623178306, 2434767459, 1623178306, 811589153]
    assert mix(lst1, 10) == [0, -2434767459, 1623178306, 3246356612, -1623178306, 2434767459, 811589153]
    # Part 2: Whole test
    assert mix2(numbers) == 1623178306

def get_solutions():
    numbers = get_numbers_from_file()
    print(mix1(numbers) == 3466)
    print(mix2(numbers) == 9995532008348)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
