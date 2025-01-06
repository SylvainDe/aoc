# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import collections

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_secrets_from_lines(string):
    return [int(l) for l in string.splitlines()]


def get_secrets_from_file(file_path=top_dir + "resources/year2024_day22_input.txt"):
    with open(file_path) as f:
        return get_secrets_from_lines(f.read())


def mix(n1, n2):
    return n1 ^ n2


def prune(n):
    return n % 16777216


def next_secret(n):
    n = prune(mix(n, n * 64))
    n = prune(mix(n, n // 32))
    n = prune(mix(n, n * 2048))
    return n


def nth_secret(secret, n):
    for i in range(n):
        secret = next_secret(secret)
    return secret


def nth_secret_sum(secrets, n):
    return sum(nth_secret(s, n) for s in secrets)


def get_max_bananas(secrets, n, nb_change=4):
    bananas = collections.Counter()
    for secret in secrets:
        change_lst = []
        changes_price = dict()
        price = secret % 10
        for i in range(n):
            secret = next_secret(secret)
            new_price = secret % 10
            change = new_price - price
            change_lst.append(change)
            last_changes = tuple(change_lst[-nb_change:])
            if last_changes not in changes_price:
                changes_price[last_changes] = new_price
            price = new_price
        for k, v in changes_price.items():
            bananas[k] += v
    return bananas.most_common(1)[0]


def run_tests():
    assert mix(42, 15) == 37
    assert prune(100000000) == 16113920
    assert next_secret(123) == 15887950
    assert next_secret(7753432) == 5908254
    nbs = [
        123,
        15887950,
        16495136,
        527345,
        704524,
        1553684,
        12683156,
        11100544,
        12249484,
        7753432,
        5908254,
    ]
    for n1, n2 in zip(nbs, nbs[1:]):
        assert next_secret(n1) == n2
    assert nth_secret(1, 2000) == 8685429
    assert nth_secret(10, 2000) == 4700978
    assert nth_secret(100, 2000) == 15273692
    assert nth_secret(2024, 2000) == 8667524
    secrets = get_secrets_from_lines(
        """1
10
100
2024"""
    )
    assert nth_secret_sum(secrets, 2000) == 37327623
    secrets = get_secrets_from_lines(
        """1
2
3
2024"""
    )
    assert get_max_bananas(secrets, n=2000) == ((-2, 1, -1, 3), 23)


def get_solutions():
    secrets = get_secrets_from_file()
    print(nth_secret_sum(secrets, 2000) == 17724064040)
    print(get_max_bananas(secrets, n=2000)[1] == 1998)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
