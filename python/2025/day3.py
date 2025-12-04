# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_bank_from_line(string):
    return string


def get_banks_from_lines(string):
    return [get_bank_from_line(l) for l in string.splitlines()]


def get_banks_from_file(file_path=top_dir + "resources/year2025_day3_input.txt"):
    with open(file_path) as f:
        return get_banks_from_lines(f.read())


def get_largest_joltage(bank, l):
    digits = ""
    for i in reversed(range(l)):
        search_space = bank[:-i] if i else bank
        d = max(search_space)
        bank = bank[bank.index(d) + 1 :]
        digits += d
    return int(digits)


def get_total_joltage(banks, l):
    return sum(get_largest_joltage(b, l) for b in banks)


def run_tests():
    banks = get_banks_from_lines(
        """987654321111111
811111111111119
234234234234278
818181911112111"""
    )
    assert get_total_joltage(banks, 2) == 357
    assert get_total_joltage(banks, 12) == 3121910778619


def get_solutions():
    banks = get_banks_from_file()
    print(get_total_joltage(banks, 2) == 17535)
    print(get_total_joltage(banks, 12) == 173577199527257)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
