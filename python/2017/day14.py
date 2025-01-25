# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import knot_hash
import collections

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_input_str_from_file(file_path=top_dir + "resources/year2017_day14_input.txt"):
    with open(file_path) as f:
        for l in f:
            return l.strip()


def hex_char_to_bits(hex_char):
    return bin(int(hex_char, 16))[2:].zfill(4)


def hex_str_to_bits(hex_str):
    s = ""
    for c in hex_str:
        s += hex_char_to_bits(c)
    return s


def get_squares(string):
    string += "-"
    ret = 0
    for i in range(128):
        ret += sum(
            b == "1" for b in hex_str_to_bits(knot_hash.knot_hash(string + str(i)))
        )
    return ret


def run_tests():
    input_str = "flqrgnkx"
    assert hex_char_to_bits("0") == "0000"
    assert hex_char_to_bits("1") == "0001"
    assert hex_char_to_bits("e") == "1110"
    assert hex_char_to_bits("f") == "1111"
    assert hex_str_to_bits("a0c2017") == "1010000011000010000000010111"
    assert get_squares(input_str) == 8108


def get_solutions():
    input_str = get_input_str_from_file()
    print(get_squares(input_str))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
