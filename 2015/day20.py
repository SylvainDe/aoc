# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import math
import itertools
import collections
import functools
import operator


def get_input_value_from_file(file_path="day20_input.txt"):
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
def get_sum_of_divisors_bigger_than(n):
    # They may be a more constructive/optimised method to
    # get numbers using the prime distinct factors formula
    for i in itertools.count(start=1):
        if sum_of_divisors_optimised(i) >= n:
            return i


def get_lowest_house_with_presents(nb):
    return get_sum_of_divisors_bigger_than(nb // 10)


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


def get_solutions():
    input_value = get_input_value_from_file()
    print(get_lowest_house_with_presents(input_value))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
