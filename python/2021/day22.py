# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import itertools
import functools
import operator

# Parse input
actions = {
    "on": True,
    "off": False,
}


def get_range(s):
    name, middle, values = s.partition("=")
    assert middle == "="
    return tuple(int(val) for val in values.split(".."))


def get_instruction_from_string(s):
    action, middle, ranges = s.partition(" ")
    assert middle == " "
    return actions[action], tuple(get_range(v) for v in ranges.split(","))


def get_instructions_from_strings(lines):
    return [get_instruction_from_string(l.strip()) for l in lines]


def get_instructions_from_file(file_path="day22_input.txt"):
    with open(file_path) as f:
        return get_instructions_from_strings(f)


# Range operations
def range_check(interval):
    begin, end = interval
    assert begin <= end


def range_intersection(interval1, interval2):
    range_check(interval1)
    range_check(interval2)
    beg1, end1 = interval1
    beg2, end2 = interval2
    beg3 = max(beg1, beg2)
    end3 = min(end1, end2)
    if beg3 <= end3:
        return range(beg3, end3 + 1)
    return []


def range_length(interval):
    range_check(interval)
    begin, end = interval
    return 1 + end - begin


def ranges_are_disjoint(interval1, interval2):
    range_check(interval1)
    range_check(interval2)
    beg1, end1 = interval1
    beg2, end2 = interval2
    return beg2 > end1 or beg1 > end2


def range_contains(interval, value):
    range_check(interval)
    begin, end = interval
    return begin <= value <= end


def range_split(interval1, interval2):
    range_check(interval1)
    range_check(interval2)
    beg1, end1 = interval1
    beg2, end2 = interval2
    # This should be easy, there are only 3 cases:
    # Case 1:
    #      +------+
    #               +------+
    #     gives:
    #      +------+
    #               +------+
    # Case 2:
    #      +------+
    #          +------+
    #     gives:
    #      +--++--+
    #          +--++--+
    # Case 3:
    #      +-------------+
    #          +------+
    #     gives:
    #      +--++------++-+
    #          +------+
    # But for the edge cases make things slightly trickier:
    #      +------+
    #             +------+
    #     gives:
    #      +-----+x
    #             x+-----+
    # Or
    #      +--------------+
    #             +
    #     gives:
    #      +-----+x+------+
    #             x
    ret1, ret2 = [], []
    midpoints = set()
    for p in [beg1, beg2, end1, end2]:
        for p2 in [p - 1, p, p + 1]:
            midpoints.add(p2)
    prevIn1, prevIn2 = False, False
    beg, end = None, None
    for p in sorted(midpoints):
        in1, in2 = (range_contains(interval1, p), range_contains(interval2, p))
        if beg is None:
            beg, end = p, p
        elif (prevIn1, prevIn2) == (in1, in2):
            end = p
        else:
            if prevIn1:
                ret1.append((beg, end))
            if prevIn2:
                ret2.append((beg, end))
            beg, end = p, p
        prevIn1, prevIn2 = in1, in2
    if prevIn1:
        ret1.append((beg, end))
    if prevIn2:
        ret2.append((beg, end))
    return ret1, ret2


# Instructions for part 1
def follow_instruction(instruction, points, interval):
    action, ranges = instruction
    ranges = [range_intersection(interval, r) for r in ranges]
    points_changed = set(itertools.product(*ranges))
    if action:
        return points | points_changed
    else:
        return points - points_changed


def follow_instructions(instructions, interval):
    points = set()
    for instruction in instructions:
        points = follow_instruction(instruction, points, interval)
    return len(points)


# Cube operations
def cube_check(cube):
    for side in cube:
        range_check(side)


def mult(iterable, start=1):
    """Returns the product of an iterable - like the sum builtin."""
    return functools.reduce(operator.mul, iterable, start)


def cube_volume(cube):
    cube_check(cube)
    return mult(range_length(side_range) for side_range in cube)


# With two cuboids A & B, we can have:
#  - A & B disjoint
#     * adding/removing is easy
#  - A entirely in B or B entirely in A
#     * adding is easy
#     * removing the big one is easy
#     * removing the small one leads to many pieces (8 in an optimal implementation, 26 in a more basic one)
#  - A & B partially overlap B
#     * a bit tedious


def cubes_are_disjoint(cube1, cube2):
    return any(ranges_are_disjoint(r1, r2) for r1, r2 in zip(cube1, cube2))


def cube_split(cube1, cube2):
    # Split the cubes by splitting the sides as much as possible
    # and then, recombine them all to form small cubes
    # TODO: This is splitting more than necessary - see comment in cube_split_tests below
    cube_check(cube1)
    cube_check(cube2)
    ret1, ret2 = [], []
    for r1, r2 in zip(cube1, cube2):
        s1, s2 = range_split(r1, r2)
        ret1.append(s1)
        ret2.append(s2)
    return list(itertools.product(*ret1)), list(itertools.product(*ret2))


# Instructions for part 2
def follow_instruction2(instruction, cubes):
    action, new_cube = instruction
    # Split existing cubes
    existing_cubes = []
    for c in cubes:
        existing_cubes.extend(cube_split(c, new_cube)[0])
    existing_cubes = set(existing_cubes)
    # Split new cube
    new_cubes = [new_cube]
    for c in existing_cubes:
        new_cubes2 = []
        for c2 in new_cubes:
            new_cubes2.extend(cube_split(c2, c)[0])
        new_cubes = new_cubes2
    new_cubes = set(new_cubes)
    # New elements are expected to be disjoints (or identical)
    if action:
        return existing_cubes | new_cubes
    else:
        return existing_cubes - new_cubes


def follow_instructions2(instructions):
    # Here we cannot store individual points because there are too many of them
    # We can try to handle disjoint cuboids containing only cubes on, the final
    # number of points is the sum of the volume of the cubes
    cubes = []
    for i, instruction in enumerate(instructions):
        # print(i + 1, len(instructions))
        cubes = follow_instruction2(instruction, cubes)
    return sum(cube_volume(c) for c in cubes)


def part1_tests():
    interval = (-50, 50)
    instructions = [get_instruction_from_string("on x=10..12,y=10..12,z=10..12")]
    assert follow_instructions(instructions, interval) == 27

    instructions = [
        "on x=10..12,y=10..12,z=10..12",
        "on x=11..13,y=11..13,z=11..13",
        "off x=9..11,y=9..11,z=9..11",
        "on x=10..10,y=10..10,z=10..10",
    ]
    instructions = get_instructions_from_strings(instructions)
    assert follow_instructions(instructions, interval) == 39

    instructions = [
        "on x=-20..26,y=-36..17,z=-47..7",
        "on x=-20..33,y=-21..23,z=-26..28",
        "on x=-22..28,y=-29..23,z=-38..16",
        "on x=-46..7,y=-6..46,z=-50..-1",
        "on x=-49..1,y=-3..46,z=-24..28",
        "on x=2..47,y=-22..22,z=-23..27",
        "on x=-27..23,y=-28..26,z=-21..29",
        "on x=-39..5,y=-6..47,z=-3..44",
        "on x=-30..21,y=-8..43,z=-13..34",
        "on x=-22..26,y=-27..20,z=-29..19",
        "off x=-48..-32,y=26..41,z=-47..-37",
        "on x=-12..35,y=6..50,z=-50..-2",
        "off x=-48..-32,y=-32..-16,z=-15..-5",
        "on x=-18..26,y=-33..15,z=-7..46",
        "off x=-40..-22,y=-38..-28,z=23..41",
        "on x=-16..35,y=-41..10,z=-47..6",
        "off x=-32..-23,y=11..30,z=-14..3",
        "on x=-49..-5,y=-3..45,z=-29..18",
        "off x=18..30,y=-20..-8,z=-3..13",
        "on x=-41..9,y=-7..43,z=-33..15",
        "on x=-54112..-39298,y=-85059..-49293,z=-27449..7877",
        "on x=967..23432,y=45373..81175,z=27513..53682",
    ]
    instructions = get_instructions_from_strings(instructions)
    assert follow_instructions(instructions, interval) == 590784


def part2_tests():
    instructions = [
        "on x=-5..47,y=-31..22,z=-19..33",
        "on x=-44..5,y=-27..21,z=-14..35",
        "on x=-49..-1,y=-11..42,z=-10..38",
        "on x=-20..34,y=-40..6,z=-44..1",
        "off x=26..39,y=40..50,z=-2..11",
        "on x=-41..5,y=-41..6,z=-36..8",
        "off x=-43..-33,y=-45..-28,z=7..25",
        "on x=-33..15,y=-32..19,z=-34..11",
        "off x=35..47,y=-46..-34,z=-11..5",
        "on x=-14..36,y=-6..44,z=-16..29",
        "on x=-57795..-6158,y=29564..72030,z=20435..90618",
        "on x=36731..105352,y=-21140..28532,z=16094..90401",
        "on x=30999..107136,y=-53464..15513,z=8553..71215",
        "on x=13528..83982,y=-99403..-27377,z=-24141..23996",
        "on x=-72682..-12347,y=18159..111354,z=7391..80950",
        "on x=-1060..80757,y=-65301..-20884,z=-103788..-16709",
        "on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856",
        "on x=-52752..22273,y=-49450..9096,z=54442..119054",
        "on x=-29982..40483,y=-108474..-28371,z=-24328..38471",
        "on x=-4958..62750,y=40422..118853,z=-7672..65583",
        "on x=55694..108686,y=-43367..46958,z=-26781..48729",
        "on x=-98497..-18186,y=-63569..3412,z=1232..88485",
        "on x=-726..56291,y=-62629..13224,z=18033..85226",
        "on x=-110886..-34664,y=-81338..-8658,z=8914..63723",
        "on x=-55829..24974,y=-16897..54165,z=-121762..-28058",
        "on x=-65152..-11147,y=22489..91432,z=-58782..1780",
        "on x=-120100..-32970,y=-46592..27473,z=-11695..61039",
        "on x=-18631..37533,y=-124565..-50804,z=-35667..28308",
        "on x=-57817..18248,y=49321..117703,z=5745..55881",
        "on x=14781..98692,y=-1341..70827,z=15753..70151",
        "on x=-34419..55919,y=-19626..40991,z=39015..114138",
        "on x=-60785..11593,y=-56135..2999,z=-95368..-26915",
        "on x=-32178..58085,y=17647..101866,z=-91405..-8878",
        "on x=-53655..12091,y=50097..105568,z=-75335..-4862",
        "on x=-111166..-40997,y=-71714..2688,z=5609..50954",
        "on x=-16602..70118,y=-98693..-44401,z=5197..76897",
        "on x=16383..101554,y=4615..83635,z=-44907..18747",
        "off x=-95822..-15171,y=-19987..48940,z=10804..104439",
        "on x=-89813..-14614,y=16069..88491,z=-3297..45228",
        "on x=41075..99376,y=-20427..49978,z=-52012..13762",
        "on x=-21330..50085,y=-17944..62733,z=-112280..-30197",
        "on x=-16478..35915,y=36008..118594,z=-7885..47086",
        "off x=-98156..-27851,y=-49952..43171,z=-99005..-8456",
        "off x=2032..69770,y=-71013..4824,z=7471..94418",
        "on x=43670..120875,y=-42068..12382,z=-24787..38892",
        "off x=37514..111226,y=-45862..25743,z=-16714..54663",
        "off x=25699..97951,y=-30668..59918,z=-15349..69697",
        "off x=-44271..17935,y=-9516..60759,z=49131..112598",
        "on x=-61695..-5813,y=40978..94975,z=8655..80240",
        "off x=-101086..-9439,y=-7088..67543,z=33935..83858",
        "off x=18020..114017,y=-48931..32606,z=21474..89843",
        "off x=-77139..10506,y=-89994..-18797,z=-80..59318",
        "off x=8476..79288,y=-75520..11602,z=-96624..-24783",
        "on x=-47488..-1262,y=24338..100707,z=16292..72967",
        "off x=-84341..13987,y=2429..92914,z=-90671..-1318",
        "off x=-37810..49457,y=-71013..-7894,z=-105357..-13188",
        "off x=-27365..46395,y=31009..98017,z=15428..76570",
        "off x=-70369..-16548,y=22648..78696,z=-1892..86821",
        "on x=-53470..21291,y=-120233..-33476,z=-44150..38147",
        "off x=-93533..-4276,y=-16170..68771,z=-104985..-24507",
    ]
    instructions = get_instructions_from_strings(instructions)
    # Check for the first steps if we get the same result for
    # original ("naive") implementation and new ("optimised")
    # implentation
    interval = (-200, 200)
    for i in range(8):
        restricted_instructions = instructions[:i]
        res1 = follow_instructions(restricted_instructions, interval)
        res2 = follow_instructions2(restricted_instructions)
        if res1 != res2:
            print(i, restricted_instructions)
            print(res1, res2)
            break
    # print(follow_instructions2(instructions))


def range_split_tests(range1, range2, expected_results=None):
    ret1, ret2 = range_split(range1, range2)
    # Elements returned are valid
    for i in ret1:
        range_check(i)
    for i in ret2:
        range_check(i)
    if ranges_are_disjoint(range1, range2):
        # Disjoint ranges are not affected
        assert ret1 == [range1]
        assert ret2 == [range2]
    elif range1 == range2:
        # Identical ranges are not affected
        assert ret1 == [range1]
        assert ret2 == [range2]
    else:
        # Overlapping different ranges are somehow affected
        len1, len2 = len(ret1), len(ret2)
        assert 1 <= len1 <= 3
        assert 1 <= len2 <= 3
        assert 3 <= len1 + len2 <= 4
        assert 2 <= len(set(ret1 + ret2)) <= 3
    # Overall length is kept
    assert sum(range_length(i) for i in ret1) == range_length(range1)
    assert sum(range_length(i) for i in ret2) == range_length(range2)
    # Individual pieces are disjoint
    for r1, r2 in itertools.permutations(ret1, 2):
        assert ranges_are_disjoint(r1, r2)
    for r1, r2 in itertools.permutations(ret2, 2):
        assert ranges_are_disjoint(r1, r2)
    # Pieces from input ranges are either identical or disjoint
    for r1, r2 in itertools.product(ret1, ret2):
        assert (r1 == r2) or ranges_are_disjoint(r1, r2)
    if expected_results is not None:
        assert (ret1, ret2) == expected_results
    elif 0:
        print(range1, range2, ret1, ret2)


def range_operation_tests():
    range0 = (10, 10)
    range1 = (0, 10)
    range2 = (10, 20)
    range3 = (20, 30)
    range4 = (5, 15)
    assert range_length(range0) == 1
    assert range_length(range1) == 11
    assert ranges_are_disjoint(range1, range3)
    assert ranges_are_disjoint(range3, range1)
    assert not ranges_are_disjoint(range1, range2)
    assert not ranges_are_disjoint(range2, range1)
    assert ranges_are_disjoint(range0, range3)
    assert ranges_are_disjoint(range3, range0)
    assert not ranges_are_disjoint(range0, range2)
    assert not ranges_are_disjoint(range2, range0)
    range_split_tests((5, 15), (0, 10), ([(5, 10), (11, 15)], [(0, 4), (5, 10)]))
    ranges = [range0, range1, range2, range3, range4]
    for r1, r2 in itertools.product(ranges, repeat=2):
        range_split_tests(r1, r2)


def cube_split_tests(cube1, cube2, expected_results=None):
    ret1, ret2 = cube_split(cube1, cube2)
    # Elements returned are valid
    for i in ret1:
        cube_check(i)
    for i in ret2:
        cube_check(i)
    if cubes_are_disjoint(cube1, cube2):
        # TODO: Disjoint cubes should not be affected
        # There may be some optimisation to be performed because we are
        # splitting more than necessary
        if 0:
            assert ret1 == [cube1]
            assert ret2 == [cube2]
    elif cube1 == cube2:
        # Identical cubes are not affected
        assert ret1 == [cube1]
        assert ret2 == [cube2]
    else:
        # Overlapping different cubes are somehow affected
        len1, len2 = len(ret1), len(ret2)
        assert 1 <= len1 <= 3 ** 3
        assert 1 <= len2 <= 3 ** 3
        assert 3 <= len1 + len2 <= 3 ** 3 + 1
        assert 2 <= len(set(ret1 + ret2)) <= 3 ** 3
    # Overall length is kept
    assert sum(cube_volume(i) for i in ret1) == cube_volume(cube1)
    assert sum(cube_volume(i) for i in ret2) == cube_volume(cube2)
    # Individual pieces are disjoint
    for c1, c2 in itertools.permutations(ret1, 2):
        assert cubes_are_disjoint(c1, c2)
    for c1, c2 in itertools.permutations(ret2, 2):
        assert cubes_are_disjoint(c1, c2)
    # Pieces from input cubes are either identical or disjoint
    for c1, c2 in itertools.product(ret1, ret2):
        assert (c1 == c2) or cubes_are_disjoint(c1, c2)
    if expected_results is not None:
        assert (ret1, ret2) == expected_results
    elif 0:
        print(cube1, cube2, ret1, ret2)


def cube_operation_tests():
    cube0 = ((0, 0), (0, 0), (0, 0))
    cube1 = ((0, 4), (0, 4), (0, 4))
    cube2 = ((0, 4), (0, 4), (0, 5))
    cube3 = ((5, 9), (5, 9), (5, 9))
    cube4 = ((5, 9), (0, 4), (0, 4))
    assert cube_volume(cube0) == 1
    assert cube_volume(cube1) == 5 * 5 * 5
    cubes = [
        cube0,
        cube1,
        cube2,
        cube3,
        cube4,
        ((1, 3), (1, 3), (1, 3)),
        ((1, 3), (0, 4), (0, 4)),
        ((1, 3), (0, 5), (0, 4)),
        ((1, 5), (1, 5), (1, 5)),
    ]
    cube_split_tests(cube0, cube1)
    cube_split_tests(cube1, cube3, ([cube1], [cube3]))
    cube_split_tests(cube0, cube4)
    for cube1, cube2 in itertools.product(cubes, repeat=2):
        assert cubes_are_disjoint(cube1, cube2) == cubes_are_disjoint(cube2, cube1)
        cube_split_tests(cube1, cube2)


def run_tests():
    range_operation_tests()
    cube_operation_tests()
    part1_tests()
    part2_tests()


def get_solutions():
    interval = (-50, 50)
    instructions = get_instructions_from_file()
    print(follow_instructions(instructions, interval))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
