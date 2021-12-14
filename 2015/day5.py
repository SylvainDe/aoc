# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import collections


def get_strings_from_file(file_path="day5_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]


def get_nb_vowels(s):
    c = collections.Counter(s)
    return sum(c[v] for v in "aeiou")


def has_double_letter(s):
    return any(c1 == c2 for c1, c2 in zip(s, s[1:]))


def is_nice(s):
    return (
        get_nb_vowels(s) >= 3
        and has_double_letter(s)
        and not any(sub in s for sub in ("ab", "cd", "pq", "xy"))
    )


def run_tests():
    assert is_nice("ugknbfddgicrmopn")
    assert is_nice("aaa")
    assert not is_nice("jchzalrnumimnmhp")
    assert not is_nice("haegwjzuvuyypxyu")
    assert not is_nice("dvszwmarrgswjxmb")


def get_solutions():
    strings = get_strings_from_file()
    print(sum(is_nice(s) for s in strings))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
