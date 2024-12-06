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
    # print(chars, groups)
    ret = get_nb_arrangements(chars, groups)
    # print(chars, groups, ret)
    return ret


import functools


@functools.lru_cache()
def get_nb_ways_split_number_in_buckets(n, nb_buckets):
    # TODO: dynamic programming
    if nb_buckets == 1:
        return 1
    if n == 0:
        return 1
    if nb_buckets == 0:
        return 0
    return sum(
        get_nb_ways_split_number_in_buckets(n - i, nb_buckets - 1) for i in range(n + 1)
    )


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
        return (
            get_nb_arrangements(chars[len(expected_beg) :], other_g)
            if suffix_matches(expected_beg, chars)
            else 0
        )
    if first_c == EMPTY:
        return get_nb_arrangements(other_c, groups)

    assert first_c == UNKNOWN
    if chars[-1] != UNKNOWN:
        return get_nb_arrangements("".join(reversed(chars)), list(reversed(groups)))

    if freedom == 0:
        cand = generate_smallest_combination(groups)
        return 1 if suffix_matches(cand, chars) else 0

    nb_full = sum(c == FULL for c in chars)
    nb_unknown = sum(c == UNKNOWN for c in chars)
    nb_empty = sum(c == EMPTY for c in chars)
    if nb_full == sum_groups:
        cand = chars.replace(UNKNOWN, EMPTY)
        return get_nb_arrangements(cand, groups)
    if nb_full > sum_groups:
        return 0
    if nb_full + nb_unknown < sum_groups:
        return 0
    if nb_full + nb_unknown == sum_groups:
        cand = chars.replace(UNKNOWN, FULL)
        return get_nb_arrangements(cand, groups)

    if nb_full + nb_empty == 0:
        return get_nb_ways_split_number_in_buckets(freedom, len(groups) + 1)

    # Divide and conquer on non-full indices
    nonfull_indices = [i for i, c in enumerate(chars) if c != FULL]
    if nonfull_indices and 0:
        mid_idx_idx = len(nonfull_indices) // 2
        assert 0 <= mid_idx_idx < len(nonfull_indices)
        mid_idx = nonfull_indices[mid_idx_idx]
        left, right = chars[:mid_idx], chars[mid_idx + 1 :]
        assert len(left) + 1 + len(right) == len(chars)
        mid_char = chars[mid_idx]
        if mid_char == UNKNOWN:
            ret = get_nb_arrangements(
                "".join(c if i != mid_idx else FULL for i, c in enumerate(chars)),
                groups,
            )
        else:
            assert mid_char == EMPTY
            ret = 0
        for i in range(len(groups) + 1):
            group_left, group_right = groups[:i], groups[i:]
            ret_left = get_nb_arrangements(left, group_left)
            if ret_left:
                ret_right = get_nb_arrangements(right, group_right)
                ret += ret_left * ret_right
        return ret

    # Divide and conquer on empty indices
    empty_indices = [i for i, c in enumerate(chars) if c == EMPTY]
    if empty_indices and 1:
        mid_idx_idx = len(empty_indices) // 2
        assert 0 <= mid_idx_idx < len(empty_indices)
        mid_idx = empty_indices[mid_idx_idx]
        left, right = chars[:mid_idx], chars[mid_idx + 1 :]
        assert chars[mid_idx] == EMPTY
        assert len(left) + 1 + len(right) == len(chars)
        ret = 0
        for i in range(len(groups) + 1):
            group_left, group_right = groups[:i], groups[i:]
            ret_left = get_nb_arrangements(left, group_left)
            if ret_left:
                ret_right = get_nb_arrangements(right, group_right)
                ret += ret_left * ret_right
        return ret

    # Divide and conquer on free indices
    free_indices = [i for i, c in enumerate(chars) if c == UNKNOWN]
    if free_indices and 1:
        mid_idx_idx = len(free_indices) // 2
        assert 0 <= mid_idx_idx < len(free_indices)
        mid_idx = free_indices[mid_idx_idx]
        left, right = chars[:mid_idx], chars[mid_idx + 1 :]
        assert chars[mid_idx] == UNKNOWN
        assert len(left) + 1 + len(right) == len(chars)
        ret = get_nb_arrangements(
            "".join(c if i != mid_idx else FULL for i, c in enumerate(chars)), groups
        )
        for i in range(len(groups) + 1):
            group_left, group_right = groups[:i], groups[i:]
            ret_left = get_nb_arrangements(left, group_left)
            if ret_left:
                ret_right = get_nb_arrangements(right, group_right)
                ret += ret_left * ret_right
        return ret

    ret = get_nb_arrangements(FULL + other_c, groups) + get_nb_arrangements(
        EMPTY + other_c, groups
    )
    return ret


def get_sum_nb_arrangement(records):
    return sum(get_nb_arrangements_wrapper(chars, groups) for chars, groups in records)


def unfold_record(record, nb):
    chars, groups = record
    return ("?".join([chars] * nb), groups * nb)


def unfold_records(records, nb=5):
    return [unfold_record(r, nb) for r in records]


def run_tests():
    assert generate_smallest_combination([]) == ""
    assert generate_smallest_combination([2]) == "##"
    assert generate_smallest_combination([2, 3, 4]) == "##.###.####"
    assert get_nb_ways_split_number_in_buckets(1, 2) == 2
    assert get_nb_ways_split_number_in_buckets(2, 2) == 3
    assert get_nb_ways_split_number_in_buckets(7, 2) == 8
    assert get_nb_ways_split_number_in_buckets(1, 3) == 3
    assert get_nb_ways_split_number_in_buckets(3, 3) == 10
    assert get_nb_ways_split_number_in_buckets(1, 5) == 5
    assert get_nb_ways_split_number_in_buckets(4, 5) == 70
    assert get_nb_ways_split_number_in_buckets(30, 11) == 847660528
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
    print(get_sum_nb_arrangement(unfold_records(records)) == 1537505634471)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
