# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import string


resource_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../resources/"

def get_dance_from_line(string):
    return string.strip().split(",")


def get_dance_from_file(file_path=resource_dir + "year2017_day16_input.txt"):
    with open(file_path) as f:
        for l in f:
            return get_dance_from_line(l)


def perform_dance(dance, progs):
    nb_prog = len(progs)
    sep = "/"
    for d in dance:
        c, arg = d[0], d[1:]
        if c == "s":
            n = int(arg)
            progs = progs[-n:] + progs[:-n]
            assert len(set(progs)) == len(progs) == nb_prog
        elif c == "x":
            arg1, mid, arg2 = arg.partition(sep)
            assert mid == sep
            i1, i2 = int(arg1), int(arg2)
            progs[i1], progs[i2] = progs[i2], progs[i1]
        elif c == "p":
            arg1, mid, arg2 = arg.partition(sep)
            assert mid == sep
            i1, i2 = progs.index(arg1), progs.index(arg2)
            progs[i1], progs[i2] = progs[i2], progs[i1]
        else:
            assert False
    assert len(set(progs)) == len(progs) == nb_prog
    return "".join(progs)


def perform_one_dance(dance, nb_prog):
    progs = list(string.ascii_lowercase[:nb_prog])
    return perform_dance(dance, progs)


def perform_many_dances(dance, nb_prog, nb_iter=1000000000):
    progs = string.ascii_lowercase[:nb_prog]
    seen = {progs: 0}
    for i in range(1, nb_iter):
        progs = perform_dance(dance, list(progs))
        if progs in seen:
            break
        seen[progs] = i
    else:
        return progs
    freq = i - seen[progs]
    rem = (nb_iter - i) % freq
    for i in range(rem):
        progs = perform_dance(dance, list(progs))
    return progs


def run_tests():
    nb_prog = 5
    dance = get_dance_from_line("s2")
    assert perform_one_dance(dance, nb_prog) == "deabc"
    dance = get_dance_from_line("s1,x3/4,pe/b")
    assert perform_one_dance(dance, nb_prog) == "baedc"


def get_solutions():
    nb_prog = 16
    dance = get_dance_from_file()
    print(perform_one_dance(dance, nb_prog) == "kpfonjglcibaedhm")
    print(perform_many_dances(dance, nb_prog) == "odiabmplhfgjcekn")


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
