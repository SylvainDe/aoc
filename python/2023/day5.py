# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import collections

# These should be dataclasses ?
Almanach = collections.namedtuple("Almanach", ("seeds", "mappings"))
Mapping = collections.namedtuple("Mapping", ("src", "dst", "ranges"))
Range = collections.namedtuple("Range", ("dst_start", "src_start", "length"))

def get_seeds_from_first_line(string):
    before, mid, seeds = string.partition("seeds: ")
    assert before == ""
    assert mid == "seeds: "
    return [int(s) for s in seeds.split()]

def get_map_from_string(string):
    lst = string.split("\n")
    name = lst[0].split(" ")[0]
    src, mid, dst = name.partition("-to-")
    assert mid == "-to-"
    return Mapping(
        src, dst,
        ranges = [Range._make(int(s) for s in r.split(" ")) for r in lst[1:] if r])

def get_almanach_from_string(string):
    parts = string.split("\n\n")
    mappings = [get_map_from_string(m) for m in parts[1:]]
    return Almanach(
        seeds = get_seeds_from_first_line(parts[0]),
        mappings = {m.src: m for m in mappings})

def get_almanach_from_file(file_path="../../resources/year2023_day5_input.txt"):
    with open(file_path) as f:
        return get_almanach_from_string(f.read())

def convert_resource_with_mapping(value, mapping):
    for dst_start, src_start, length in mapping.ranges:
        src_end = src_start + length
        if src_start <= value < src_end:
            return value - src_start + dst_start
    return value

def convert_small_range_with_mapping(small_range, mapping):
    beg, end = small_range
    for dst_start, src_start, length in mapping.ranges:
        src_end = src_start + length
        beg_in_range = src_start <= beg < src_end
        end_in_range = src_start <= end < src_end
        assert beg_in_range == end_in_range
        if beg_in_range:
            shift = dst_start - src_start
            return (beg + shift, end + shift)
    return small_range

def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return zip(a, a)

def convert_ranges_with_mapping(ranges, mapping):
    # Find limits
    limits = set()
    for _, src_start, length in mapping.ranges:
        src_end = src_start + length
        limits.add(src_start)
        limits.add(src_end)
    limits = sorted(limits)
    # Split ranges on limits
    for l in limits:
        new_ranges = set()
        for beg, end in ranges:
            if beg < l <= end:
                new_ranges.add((beg, l-1))
                new_ranges.add((l, end))
            else:
                new_ranges.add((beg, end))
        ranges = new_ranges
    # Convert ranges
    return set(convert_small_range_with_mapping(r, mapping) for r in ranges)

def get_locations_for_seeds(almanach):
    res, res_name = set(almanach.seeds), "seed"
    mappings = almanach.mappings
    while res_name in mappings:
        m = mappings[res_name]
        res = set(convert_resource_with_mapping(r, m) for r in res)
        res_name = m.dst
    assert res_name == "location"
    return res

def get_locations_for_seed_ranges(almanach):
    res_name = "seed"
    res = [(start, start + length) for start, length in pairwise(almanach.seeds)]
    mappings = almanach.mappings
    while res_name in mappings:
        m = mappings[res_name]
        res = convert_ranges_with_mapping(res, m)
        res_name = m.dst
    assert res_name == "location"
    return res

def run_tests():
    almanach = get_almanach_from_string(
        """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""
    )
    assert min(get_locations_for_seeds(almanach)) == 35
    assert min(get_locations_for_seed_ranges(almanach))[0] == 46


def get_solutions():
    almanach = get_almanach_from_file()
    print(min(get_locations_for_seeds(almanach)) == 251346198)
    print(min(get_locations_for_seed_ranges(almanach))[0] == 72263011)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
