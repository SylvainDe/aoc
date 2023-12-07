# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import collections
import itertools


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"

def get_boxes_from_file(file_path=top_dir + "resources/year2018_day2_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]


def get_checksum(boxes):
    nb2, nb3 = 0, 0
    for box in boxes:
        c = collections.Counter(box)
        nb2 += 2 in c.values()
        nb3 += 3 in c.values()
    return nb2 * nb3


def find_common_chars(boxes):
    for b1, b2 in itertools.combinations(boxes, 2):
        if len(b1) == len(b2):
            common = [c1 for c1, c2 in zip(b1, b2) if c1 == c2]
            if len(common) + 1 == len(b1):
                return "".join(common)


def run_tests():
    boxes = ["abcdef", "bababc", "abbcde", "abcccd", "aabcdd", "abcdee", "ababab"]
    assert get_checksum(boxes) == 12


def get_solutions():
    boxes = get_boxes_from_file()
    print(get_checksum(boxes) == 7657)
    print(find_common_chars(boxes) == "ivjhcadokeltwgsfsmqwrbnuy")


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
