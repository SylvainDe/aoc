# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_passphrases_from_file(file_path="day4_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]


def passphrase_is_valid(s):
    lst = s.split(" ")
    return len(lst) == len(set(lst))


def run_tests():
    assert passphrase_is_valid("aa bb cc dd ee")
    assert not passphrase_is_valid("aa bb cc dd aa")
    assert passphrase_is_valid("aa bb cc dd aaa")


def get_solutions():
    passphrases = get_passphrases_from_file()
    print(sum(passphrase_is_valid(s) for s in passphrases))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
