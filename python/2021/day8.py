# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import collections


def get_signals_from_str(l, sep=" | "):
    left, mid, right = l.strip().partition(sep)
    assert mid == sep
    return (left.split(), right.split())


def get_signals_from_file(file_path="day8_input.txt"):
    with open(file_path) as f:
        return [get_signals_from_str(l) for l in f]


RAW_SEGMENTS = [
    # A, B, C, D, E, F, G
    (1, 1, 1, 0, 1, 1, 1),
    (0, 0, 1, 0, 0, 1, 0),
    (1, 0, 1, 1, 1, 0, 1),
    (1, 0, 1, 1, 0, 1, 1),
    (0, 1, 1, 1, 0, 1, 0),
    (1, 1, 0, 1, 0, 1, 1),
    (1, 1, 0, 1, 1, 1, 1),
    (1, 0, 1, 0, 0, 1, 0),
    (1, 1, 1, 1, 1, 1, 1),
    (1, 1, 1, 1, 0, 1, 1),
]


def print_segments():
    """Ensure that the segment segments values are correct."""
    h = {0: "  ", 1: "--"}
    v = {0: " ", 1: "|"}
    for a, b, c, d, e, f, g in RAW_SEGMENTS:
        print(" %s" % (h[a]))
        print("%s %s" % (v[b], v[c]))
        print(" %s" % (h[d]))
        print("%s %s" % (v[e], v[f]))
        print(" %s" % (h[g]))
        print()


LETTERS = "ABCDEFG"

SEGMENTS = {
    "".join(letter for bit, letter in zip(s, LETTERS) if bit): i
    for i, s in enumerate(RAW_SEGMENTS)
}


def group_by_len(strs):
    lengths = dict()
    for s in strs:
        lengths.setdefault(len(s), []).append(s)
    return lengths


SEGMENTS_BY_LEN = group_by_len(SEGMENTS.keys())


def signal_can_be_segment(signal, segment, mapping):
    if len(signal) != len(segment):
        return False
    for l, decoded_set in mapping.items():
        if not any((s in segment) == (l in signal) for s in decoded_set):
            return False
    return True


def decode_signal_pattern(signals):
    mapping = {l: set(L for L in LETTERS) for l in LETTERS.lower()}
    signals = ["".join(sorted(sig)) for sig in signals]
    lengths = group_by_len(signals)
    for i in sorted(lengths):
        sig_i, seg_i = lengths[i], SEGMENTS_BY_LEN[i]
        assert len(sig_i) == len(seg_i)
        seg_values = set.union(*(set(seg) for seg in seg_i))
        sig_values = set.union(*(set(sig) for sig in sig_i))
        for l in sig_values:
            mapping[l] = mapping[l].intersection(seg_values)
    change = True
    while change:
        change = False
        equivalent_map = dict()
        for l, letters in mapping.items():
            equivalent_map.setdefault(tuple(letters), []).append(l)
        for lletters, uletters in equivalent_map.items():
            # If for instance 3 letters map to 3 letters, these can't be anywhere else
            if len(lletters) == len(uletters):
                for l, letters in mapping.items():
                    if tuple(letters) != lletters:
                        for c in lletters:
                            if c in letters:
                                change = True
                                letters.remove(c)
    # At this stage, everything is done and ready to be used
    signal_to_segment = dict()
    for sig in signals:
        for seg in SEGMENTS:
            if signal_can_be_segment(sig, seg, mapping):
                assert sig not in signal_to_segment
                signal_to_segment[sig] = seg
    return signal_to_segment


def decode_signal(signal):
    left, right = signal
    # Use left to get decoding mapping
    signal_to_segment = decode_signal_pattern(left)
    # And apply it on right
    for r in right:
        yield SEGMENTS[signal_to_segment["".join(sorted(r))]]


def decode_signals(signals):
    c = collections.Counter(d for s in signals for d in decode_signal(s))
    return c[1] + c[4] + c[7] + c[8]


def decode_signals2(signals):
    return sum(int("".join(str(d) for d in decode_signal(s))) for s in signals)


def run_tests():
    signals = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"
    signals = [get_signals_from_str(signals)]
    assert decode_signals(signals) == 0
    signals = [
        "be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe",
        "edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc",
        "fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg",
        "fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb",
        "aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea",
        "fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb",
        "dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe",
        "bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef",
        "egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb",
        "gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce",
    ]
    signals = [get_signals_from_str(s) for s in signals]
    assert decode_signals(signals) == 26
    assert decode_signals2(signals) == 61229


def get_solutions():
    signals = get_signals_from_file()
    print(decode_signals(signals))
    print(decode_signals2(signals))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
