# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_numbers_from_file(file_path="../../resources/year2020_day9_input.txt"):
    with open(file_path) as f:
        return [int(l) for l in f]


def find_pair_sum(numbers, n):
    for p1 in numbers:
        p2 = n - p1
        if p2 in numbers:
            return True
    return False


def find_first_counterexample(numbers, preamble_size):
    for i in range(preamble_size, len(numbers)):
        n = numbers[i]
        if not find_pair_sum(set(numbers[i - preamble_size : i]), n):
            return n
    return None


def find_contiguous_set_with_sum(numbers, n):
    for i in range(len(numbers)):
        curr_sum = 0
        for j in range(i, len(numbers)):
            curr_sum += numbers[j]
            if curr_sum == n:
                return numbers[i : j + 1]
            elif curr_sum > n:
                break
    return None


def solution_for_part2(numbers, preamble_size):
    counter_ex = find_first_counterexample(numbers, preamble_size)
    contiguous_elts = find_contiguous_set_with_sum(numbers, counter_ex)
    return max(contiguous_elts) + min(contiguous_elts)


def run_tests():
    example = [
        35,
        20,
        15,
        25,
        47,
        40,
        62,
        55,
        65,
        95,
        102,
        117,
        150,
        182,
        127,
        219,
        299,
        277,
        309,
        576,
    ]
    assert find_first_counterexample(example, 5) == 127
    assert find_contiguous_set_with_sum(example, 127) == [15, 25, 47, 40]
    assert solution_for_part2(example, 5) == 62


def get_solutions():
    numbers = get_numbers_from_file()
    print(find_first_counterexample(numbers, 25) == 70639851)
    print(solution_for_part2(numbers, 25) == 8249240)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
