# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_lst_from_line(string):
    return string.split(",")


def get_lst_from_file(file_path=top_dir + "resources/year2023_day15_input.txt"):
    with open(file_path) as f:
        for l in f:
            return get_lst_from_line(l.strip())

def get_hash(string):
    val = 0
    for c in string:
        val = (17 * (val + ord(c))) % 256
    return val

def get_hash_sum(lst):
    return sum(get_hash(l) for l in lst)


def get_focusing_power_sum(lst):
    boxes = [list() for _ in range(255)]
    for lens in lst:
        label, nb = (lens[:-1], None) if lens.endswith("-") else lens.split("=")
        box = boxes[get_hash(label)]
        idx = next((i for i, (l, _) in enumerate(box) if l == label), None)
        if idx is not None:
            box.pop(idx)
        if nb is not None:
            box.insert(len(box) if idx is None else idx, (label, int(nb)))
    return sum(
        i * j * nb
        for i, box_lst in enumerate(boxes, start=1)
        for j, (_, nb) in enumerate(box_lst, start=1))


def run_tests():
    lst = get_lst_from_line("rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7")
    assert get_hash_sum(lst) == 1320
    assert get_focusing_power_sum(lst) == 145


def get_solutions():
    lst = get_lst_from_file()
    print(get_hash_sum(lst) == 511416)
    print(get_focusing_power_sum(lst) == 290779)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
