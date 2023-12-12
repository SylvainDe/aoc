# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


EMPTY = "."
UNKNOWN = "?"
FULL = "#"
KNOWN_VALUES = {EMPTY, FULL}
VALID_VALUES = {EMPTY, FULL, UNKNOWN}

def get_record_from_line(string):
    chars, groups = string.split()
    return chars, [int(s) for s in groups.split(",")]


def get_records_from_lines(string):
    return [get_record_from_line(l) for l in string.splitlines()]


def get_records_from_file(file_path=top_dir + "resources/year2023_day12_input.txt"):
    with open(file_path) as f:
        return get_records_from_lines(f.read())


def suffix_matches(suffix, chars):
    assert len(suffix) <= len(chars)
    for s, c in zip(suffix, chars):
        assert s in KNOWN_VALUES
        assert c in VALID_VALUES
        if c != UNKNOWN and c != s:
            return False
    return True


def generate_smallest_combination(groups):
    ret = []
    for nb in groups:
        ret.extend([FULL] * nb + [EMPTY])
    return "".join(ret[:-1])


def get_nb_arrangements_wrapper(chars, groups):
    ret = get_nb_arrangements(chars, groups)
    print(chars, groups, ret)
    return ret

def get_nb_arrangements(chars, groups):
    if not groups:
        return 0 if FULL in chars else 1
    if not chars:
        return 0

    sum_groups = sum(groups)
    min_blocks = sum_groups + len(groups) - 1
    freedom = len(chars) - min_blocks
    if freedom < 0:
        return 0

    first_c, other_c = chars[0], chars[1:]
    first_g, other_g = groups[0], groups[1:]
    if first_c == FULL:
        expected_beg = "".join([FULL] * first_g + ([EMPTY] if other_g else []))
        return get_nb_arrangements(chars[len(expected_beg):], other_g) \
            if suffix_matches(expected_beg, chars) else 0
    if first_c == EMPTY:
        return get_nb_arrangements(other_c, groups)

    assert first_c == UNKNOWN
    if chars[-1] != UNKNOWN:
        return get_nb_arrangements("".join(reversed(chars)), list(reversed(groups)))

    if freedom == 0:
        cand = generate_smallest_combination(groups)
        return 1 if suffix_matches(cand, chars) else 0

    # nb_full = sum(c == FULL for c in chars)
    # nb_unknown = sum(c == UNKNOWN for c in chars)
    # nb_empty = sum(c == EMPTY for c in chars)
    # if nb_full == sum_groups:
    #     cand = chars.replace(UNKNOWN, EMPTY)
    #     return get_nb_arrangements(cand, groups)
    # if nb_full > sum_groups:
    #     return 0
    # if nb_full + nb_unknown < sum_groups:
    #     return 0
    # if nb_full + nb_unknown == sum_groups:
    #     cand = chars.replace(UNKNOWN, FULL)
    #     return get_nb_arrangements(cand, groups)
    ret = get_nb_arrangements(FULL + other_c, groups) + get_nb_arrangements(EMPTY + other_c, groups)
    # if nb_full + nb_empty == 0:
    #     # print(chars, groups, freedom, ret)
    #     pass # There is an optimisation to be found here
    return ret


def get_sum_nb_arrangement(records):
    return sum(get_nb_arrangements_wrapper(chars, groups) for chars, groups in records)

def unfold_record(record, nb):
    chars, groups = record
    return ("?".join([chars] *nb), groups * nb)

def unfold_records(records, nb=5):
    return [unfold_record(r, nb) for r in records]

def run_tests():
    assert generate_smallest_combination([]) == ""
    assert generate_smallest_combination([2]) == "##"
    assert generate_smallest_combination([2, 3, 4]) == "##.###.####"
    records = get_records_from_lines(
        """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""
    )
    assert get_sum_nb_arrangement(records) == 21
    assert get_sum_nb_arrangement(unfold_records(records)) == 525152


def get_solutions():
    records = get_records_from_file()
    print(get_sum_nb_arrangement(records) == 6827)
    # print(get_sum_nb_arrangement(unfold_records(records)))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
