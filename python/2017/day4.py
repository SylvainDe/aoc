# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_passphrases_from_file(file_path=top_dir + "resources/year2017_day4_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]


def passphrase_is_valid(s):
    lst = s.split(" ")
    return len(lst) == len(set(lst))


def passphrase_is_valid2(s):
    lst = ["".join(sorted(w)) for w in s.split(" ")]
    return len(lst) == len(set(lst))


def run_tests():
    assert passphrase_is_valid("aa bb cc dd ee")
    assert not passphrase_is_valid("aa bb cc dd aa")
    assert passphrase_is_valid("aa bb cc dd aaa")
    assert passphrase_is_valid2("abcde fghij")
    assert not passphrase_is_valid2("abcde xyz ecdab")
    assert passphrase_is_valid2("iiii oiii ooii oooi oooo")


def get_solutions():
    passphrases = get_passphrases_from_file()
    print(sum(passphrase_is_valid(s) for s in passphrases) == 451)
    print(sum(passphrase_is_valid2(s) for s in passphrases) == 223)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
