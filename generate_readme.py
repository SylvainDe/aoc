"""Script to generate README.

Usage: python3 generate_readme.py > README.md
"""
import os

# Separator
sep = "|"

# URLs
puzzle_url = "[Problem](https://adventofcode.com/{year}/day/{day})"
input_url = "[Input](https://adventofcode.com/{year}/day/{day}/input)"
urls = (puzzle_url, input_url)

# Local files
puzzle_file = "resources/year{year}_day{day}_puzzle.txt"
input_file = "resources/year{year}_day{day}_input.txt"
python_file = "python/{year}/day{day}.py"
rust_file = "rust/src/{year}/day{day}/main.rs"
files = (puzzle_file, input_file, python_file, rust_file)

# Header
header = """# aoc

Solutions for Advent Of Code

Solutions used to be stored in different repositories for each year limiting the code reuse:
 - https://github.com/SylvainDe/aoc2019
 - https://github.com/SylvainDe/aoc2020
 - https://github.com/SylvainDe/aoc2021

Solutions are written in Python and/or Rust.
"""

def file_contains(filepath, string):
    with open(filepath) as f:
        for line in f:
            if string in line:
                return True
    return False


def file_count_lines(filepath, string):
    with open(filepath) as f:
        return sum(string in line for line in f)
    return 0


def format_file(filepath):
    if not os.path.isfile(filepath):
        return ""
    name_shown = os.path.basename(filepath)
    if filepath.endswith("puzzle.txt"):
        name_shown = "puzzle.txt"
        count_stars = file_count_lines(filepath, "<p>Your puzzle answer was <code>")
        if count_stars:
            name_shown += " " + "*" * count_stars
    if filepath.endswith("input.txt"):
        name_shown = "input.txt"
    elif filepath.endswith(".py") and file_contains(filepath, "xxx = get_xxx_from_file"):
        name_shown = "not solved"
    elif filepath.endswith(".rs") and file_contains(filepath, "fn part1(_arg"):
        name_shown = "not solved"
    return "[{name_shown}]({fullpath})".format(name_shown=name_shown, fullpath=filepath)

def format_table_colums(columns):
    return "{}{}{}".format(sep, sep.join(columns), sep)

# Generation
print(header)
columns = ["Year", "Day", "URLs", "Puzzle", "Input", "Python", "Rust"]
print(format_table_colums(columns))
print(format_table_colums(("---" for _ in columns)))
for year in range(2015, 2021+1):
    for day in range(1, 25+1):
        day_urls = [" ".join([u.format(year=year, day=day) for u in urls])]
        day_files = [format_file(f.format(year=year, day=day)) for f in files]
        columns = [str(year), str(day)] + day_urls + day_files
        print(format_table_colums(columns))
    print(format_table_colums(("-" for _ in columns)))

