# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import heapq

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_diskmap_from_file(file_path=top_dir + "resources/year2024_day9_input.txt"):
    with open(file_path) as f:
        for l in f:
            return l.strip()


def generate_files(diskmap):
    for i, n in enumerate(diskmap):
        q, r = divmod(i, 2)
        yield (q if r == 0 else None, int(n))


def part1(diskmap):
    fs = []
    for f, l in generate_files(diskmap):
        fs.extend([f] * l)
    free_idx = 0
    end_idx = len(fs) - 1
    while True:
        while free_idx < end_idx and fs[free_idx] is not None:
            free_idx += 1
        while free_idx < end_idx and fs[end_idx] is None:
            end_idx -= 1
        if free_idx >= end_idx:
            break
        fs[free_idx], fs[end_idx] = fs[end_idx], fs[free_idx]
    return sum(i * n for i, n in enumerate(fs) if n is not None)


def part2(diskmap):
    free = []
    files = []
    pos = 0
    for f, l in generate_files(diskmap):
        if f is None:
            free.append((pos, l))
        else:
            files.append((pos, l, f))
        pos += l
    ret_sum = 0
    for (f_pos, f_l, f_val) in reversed(files):
        for i, (free_pos, free_l) in enumerate(free):
            if f_pos < free_pos:
                break
            if free_l >= f_l:
                # Big enough
                f_pos = free_pos
                free.pop(i)
                if free_l > f_l:
                    free.append((f_pos + f_l, free_l - f_l))
                    free.sort()
                break
        ret_sum += f_val * sum(f_pos + i for i in range(f_l))
    return ret_sum


def run_tests():
    diskmap = "2333133121414131402"
    assert part1(diskmap) == 1928
    assert part2(diskmap) == 2858


def get_solutions():
    diskmap = get_diskmap_from_file()
    print(part1(diskmap) == 6334655979668)
    print(part2(diskmap) == 6349492251099)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
