# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import math
import itertools
import collections
import functools
import operator


def get_input_value_from_file(file_path="../../resources/year2015_day20_input.txt"):
    with open(file_path) as f:
        for l in f:
            return int(l.strip())


# Various functions based on divisors and primes


def mult(iterable, start=1):
    """Returns the product of an iterable - like the sum builtin."""
    return functools.reduce(operator.mul, iterable, start)


def yield_divisors_using_divisions(n):
    """Yields distinct divisors of n.

    This uses sucessive divisions so it can be slower than
    yield_divisors_using_primes_factorisation on big inputs but it is easier
    to understand, the upper bound of O(sqrt(n)) is guarantee and faster on
    small inputs."""
    assert n > 0
    yield 1
    if n > 1:
        yield n
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                j = n // i
                yield i
                if i != j:
                    yield j


def prime_factors(n):
    """Yields prime factors of a positive number."""
    assert n > 0
    d = 2
    while d * d <= n:
        while n % d == 0:
            n //= d
            yield d
        d += 1
    if n > 1:  # to avoid 1 as a factor
        assert d <= n
        yield n


def yield_divisors_using_primes_factorisation(n):
    """Yields distinct divisors of n.

    This uses the prime factorisation to generate the different divisors.
    It is faster than yield_divisors_using_divisions on most big inputs
    but the complexity is hard to guarantee on all inputs and it is slower
    on small inputs."""
    elements = (
        [p ** power for power in range(c + 1)]
        for p, c in collections.Counter(prime_factors(n)).items()
    )
    return (mult(it) for it in itertools.product(*elements))


# https://en.wikipedia.org/wiki/Divisor_function
def sum_of_divisors_naive(n):
    return sum(yield_divisors_using_divisions(n))


def sum_of_divisors_optimised(n):
    return mult(
        ((p ** (c + 1) - 1) / (p - 1))
        for p, c in collections.Counter(prime_factors(n)).items()
    )


# https://en.wikipedia.org/wiki/Highly_abundant_number
def get_naive_sum_of_divisors_bigger_than(n):
    for i in itertools.count(start=1):
        if sum_of_divisors_optimised(i) >= n:
            return i


def get_optimised_sum_of_divisors_bigger_than(n):
    # Get numbers of divisors using the prime distinct factors formula
    # sigma(n) > X
    # _____    ai + 1
    #  | |   pi       - 1
    #  | |  ------------  > X
    #  | |      pi  - 1
    if n < 2:
        return 1
    candidate = None
    values = [(1, 1)]  # (i, sigma(i)) with sigma(i) < n
    # TODO: We are missing a condition to stop checking more primes
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67]:  # TODO
        new_values = []
        for power in itertools.count(start=1):
            new_value_added = False
            p_pow = p ** power
            coef, remaining = divmod(p_pow * p - 1, p - 1)
            assert remaining == 0
            for (prod, sum_div) in values:
                prod2, sum_div2 = prod * p_pow, sum_div * coef
                cand2 = prod2, sum_div2
                if candidate is None or prod2 <= candidate:
                    if sum_div2 >= n:
                        candidate = prod2
                    else:
                        new_values.append(cand2)
                        new_value_added = True
            if not new_value_added:
                break
        values.extend(new_values)
    return candidate


def get_lowest_house_with_presents(nb):
    return get_optimised_sum_of_divisors_bigger_than(nb // 10)


def run_tests():
    tests = [
        (1, 1),
        (2, 3),
        (3, 4),
        (4, 7),
        (5, 6),
        (6, 12),
        (7, 8),
        (8, 15),
        (9, 13),
    ]
    for n, s in tests:
        assert sum_of_divisors_naive(n) == s
        assert sum_of_divisors_optimised(n) == s
    assert get_lowest_house_with_presents(140) == 8
    assert get_lowest_house_with_presents(120) == 6
    for val in list(range(0, 10)) + list(range(100, 110)) + list(range(1000, 1100)):
        naive = get_naive_sum_of_divisors_bigger_than(val)
        optimised = get_optimised_sum_of_divisors_bigger_than(val)
        assert naive == optimised


def get_solutions():
    input_value = get_input_value_from_file()
    print(get_lowest_house_with_presents(input_value))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
