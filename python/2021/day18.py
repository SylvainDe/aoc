# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import itertools


def get_pair_from_str(s):
    digits = []
    pair = []
    depth = 0
    for c in s:
        if c.isdigit():
            digits.append(c)
        else:
            if digits:
                pair.append((int("".join(digits)), depth))
                digits = []
            if c == "[":
                depth += 1
            elif c == "]":
                depth -= 1
            elif c == ",":
                pair.append((c, depth))
    assert digits == []
    return pair


def get_pairs_from_file(file_path="day18_input.txt"):
    with open(file_path) as f:
        return [get_pair_from_str(l.strip()) for l in f]


def explode(pair):
    for i, (val, depth) in enumerate(pair):
        assert (isinstance(val, int)) == (i % 2 == 0)
        assert (val == ",") == (i % 2 == 1)
        if i % 2 == 0:
            if depth >= 5:
                assert depth == 5
                assert 0 <= i + 2 < len(pair)
                val2, depth2 = pair[i + 2]
                assert depth == depth2
                if 0 <= i - 2 < len(pair):
                    val3, depth3 = pair[i - 2]
                    pair[i - 2] = (val3 + val, depth3)
                if 0 <= i + 4 < len(pair):
                    val3, depth3 = pair[i + 4]
                    pair[i + 4] = (val3 + val2, depth3)
                pair.pop(i)
                pair.pop(i)
                pair[i] = (0, depth - 1)
                return True
    return False


def split(pair):
    for i, (val, depth) in enumerate(pair):
        assert (isinstance(val, int)) == (i % 2 == 0)
        assert (val == ",") == (i % 2 == 1)
        if i % 2 == 0 and val >= 10:
            new_depth = depth + 1
            half, rem = divmod(val, 2)
            left, right = half, half + rem
            pair.pop(i)
            pair.insert(i, (right, new_depth))
            pair.insert(i, (",", new_depth))
            pair.insert(i, (left, new_depth))
            return True
    return False


def reduce_pair(pair):
    while True:
        if explode(pair):
            continue
        if split(pair):
            continue
        break


def add_pair(pair1, pair2):
    pair = (
        [(val, depth + 1) for val, depth in pair1]
        + [(",", 1)]
        + [(val, depth + 1) for val, depth in pair2]
    )
    reduce_pair(pair)
    return pair


def add_pairs(lst):
    res = None
    for pair in lst:
        if res is None:
            res = pair
        else:
            res = add_pair(res, pair)
    return res


def magnitude(pair, depth_arg=1):
    if len(pair) == 1:
        val, depth = pair[0]
        assert isinstance(val, int)
        return val
    coma = None
    for i, (val, depth) in enumerate(pair):
        assert (isinstance(val, int)) == (i % 2 == 0)
        assert (val == ",") == (i % 2 == 1)
        if val == "," and depth == depth_arg:
            assert coma is None
            coma = i
    assert coma is not None
    left = pair[0:coma]
    right = pair[coma + 1 :]
    return 3 * magnitude(left, depth_arg + 1) + 2 * magnitude(right, depth_arg + 1)


def string_handling_tests():
    tests = [
        "[[[[[9,8],1],2],3],4]",
        "[7,[6,[5,[4,[3,2]]]]]",
        "[[6,[5,[4,[3,2]]]],1]",
        "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]",
        "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]",
        "[[9,1],[1,9]]",
    ]
    for s in tests:
        pair = get_pair_from_str(s)


def explode_tests():
    tests = [
        ("[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]"),
        ("[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]"),
        ("[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]"),
        ("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"),
        ("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"),
    ]
    for s1, s2 in tests:
        pair = get_pair_from_str(s1)
        assert explode(pair)
        assert pair == get_pair_from_str(s2)


def split_tests():
    tests = [
        ("[[[[0,7],4],[15,[0,13]]],[1,1]]", "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]"),
        ("[[[[0,7],4],[[7,8],[0,13]]],[1,1]]", "[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]"),
    ]
    for s, s2 in tests:
        pair = get_pair_from_str(s)
        assert split(pair)
        assert pair == get_pair_from_str(s2)


def reduce_tests():
    s = "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]"
    s2 = "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
    pair = get_pair_from_str(s)
    reduce_pair(pair)
    assert pair == get_pair_from_str(s2)


def add_tests():
    p1 = get_pair_from_str("[[[[4,3],4],4],[7,[[8,4],9]]]")
    p2 = get_pair_from_str("[1,1]")
    pair = add_pair(p1, p2)
    pair2 = get_pair_from_str("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")
    assert pair == pair2


def adds_tests():
    lst = ["[1,1]", "[2,2]", "[3,3]", "[4,4]", "[5,5]"]
    pairs = [get_pair_from_str(s) for s in lst]
    pair = add_pairs(pairs)
    pair2 = get_pair_from_str("[[[[3,0],[5,3]],[4,4]],[5,5]]")
    assert pair == pair2


def magnitude_tests():
    tests = [
        ("[9,1]", 29),
        ("[1,9]", 21),
        ("[[9,1],[1,9]]", 129),
        ("[[1,2],[[3,4],5]]", 143),
        ("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", 1384),
        ("[[[[1,1],[2,2]],[3,3]],[4,4]]", 445),
        ("[[[[3,0],[5,3]],[4,4]],[5,5]]", 791),
        ("[[[[5,0],[7,4]],[5,5]],[6,6]]", 1137),
        ("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", 3488),
    ]
    for s, m in tests:
        pair = get_pair_from_str(s)
        assert magnitude(pair) == m


def run_tests():
    string_handling_tests()
    explode_tests()
    split_tests()
    reduce_tests()
    add_tests()
    adds_tests()
    magnitude_tests()


def get_solutions():
    pairs = get_pairs_from_file()
    pair = add_pairs(pairs)
    print(magnitude(pair))
    print(max(magnitude(add_pair(a, b)) for a, b in itertools.permutations(pairs, 2)))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
