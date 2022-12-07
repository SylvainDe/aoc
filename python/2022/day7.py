# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import collections

def get_lines_from_file(file_path="../../resources/year2022_day7_input.txt"):
    with open(file_path) as f:
       return [l.strip() for l in f]

def get_list_of_files(lines):
    files = dict()
    cwd = []
    for l in lines:
        chunks = l.split(" ")
        if chunks[0] == "$":
            # Command
            cmd = chunks[1]
            if cmd == "cd":
                arg = chunks[2]
                if arg == "/":
                    cwd.clear()
                elif arg == "..":
                    cwd.pop()
                else:
                    cwd.append(arg)
            else:
                assert cmd == "ls"
        elif chunks[0] == "dir":
            pass
        else:
            size, name = chunks
            size = int(size)
            files[tuple(cwd + [name])] = size
    return files

def find_directories(files):
    directories = collections.Counter()
    for path, size in files.items():
        for i in range(len(path)-1):
            dir_path = path[:i+1]
            directories[dir_path] += size
    return directories

def find_biggest_small_directories(lines):
    files = get_list_of_files(lines)
    small_dirs = {
        name:size
        for name, size in find_directories(files).items()
        if size < 100000
    }
    return sum(small_dirs.values())

def find_dir_to_remove(lines, total_space=70000000, need=30000000):
    files = get_list_of_files(lines)
    space_used = sum(files.values())
    free_space = total_space - space_used
    space_to_free = need - free_space
    assert space_to_free >= 0
    big_dirs = collections.Counter({
        name:size
        for name, size in find_directories(files).items()
        if size >= space_to_free
    })
    return big_dirs.most_common()[-1][-1]

def run_tests():
    lines = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k""".splitlines()
    assert find_biggest_small_directories(lines) == 95437
    assert find_dir_to_remove(lines) == 24933642

def get_solutions():
    lines = get_lines_from_file()
    print(find_biggest_small_directories(lines) == 1348005)
    print(find_dir_to_remove(lines) == 12785886)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
