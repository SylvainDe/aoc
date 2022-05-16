# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import collections


def get_diag_from_file(file_path="day3_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]


other_bit = {"0": "1", "1": "0"}


def get_power_consumption(diagnostic):
    gamma, epsilon = "", ""
    for i in range(len(diagnostic[0])):
        c = collections.Counter(diag[i] for diag in diagnostic)
        val, nb = c.most_common(1)[0]
        gamma += val
        epsilon += other_bit[val]
    return int(gamma, base=2) * int(epsilon, base=2)


def oxygen_rating(diagnostic, i):
    c = collections.Counter(diag[i] for diag in diagnostic)
    # Dirty hack to ensure that most_common(2) has something to return
    c["1"] += 0
    c["0"] += 0
    (val1, nb1), (val2, nb2) = c.most_common(2)
    if nb1 == nb2:
        return "1"
    return val1


def co2_rating(diagnostic, i):
    return other_bit[oxygen_rating(diagnostic, i)]


def apply_bit_criteria(diagnostic, function):
    for i in range(len(diagnostic[0])):
        if len(diagnostic) == 1:
            break
        bit_val = function(diagnostic, i)
        diagnostic = [diag for diag in diagnostic if diag[i] == bit_val]
    if len(diagnostic) != 1:
        print("Warning: expected 1 remaining diag, got %d" % len(diagnostic))
    return diagnostic[0]


def get_life_support_rating(diagnostic):
    oxygen = apply_bit_criteria(diagnostic, oxygen_rating)
    co2 = apply_bit_criteria(diagnostic, co2_rating)
    return int(oxygen, base=2) * int(co2, base=2)


def run_tests():
    diag = [
        "00100",
        "11110",
        "10110",
        "10111",
        "10101",
        "01111",
        "00111",
        "11100",
        "10000",
        "11001",
        "00010",
        "01010",
    ]
    assert get_power_consumption(diag) == 198
    assert get_life_support_rating(diag) == 230


def get_solutions():
    diag = get_diag_from_file()
    print(get_power_consumption(diag))
    print(get_life_support_rating(diag))
    diag = get_diag_from_file("day3_input2.txt")
    print(get_power_consumption(diag))
    print(get_life_support_rating(diag))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
