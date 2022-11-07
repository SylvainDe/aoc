"""Script to generate README.

Usage: python3 generate_readme.py > README.md
"""
import os

# Separator
sep = "|"

# URLs
puzzle_url = "[Problem](https://adventofcode.com/{year}/day/{day})"
input_url = "[Input](https://adventofcode.com/{year}/day/{day}/input)"

# Local files
puzzle_file = "resources/year{year}_day{day}_puzzle.txt"
input_file = "resources/year{year}_day{day}_input.txt"
python_file = "python/{year}/day{day}.py"
rust_file = "rust/src/{year}/day{day}/main.rs"

# Date
date = "{year}/{day}"

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
    elif filepath.endswith("input.txt"):
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
columns = ["Date", "URLs", "Puzzle & Input", "Stars", "Python", "Rust"]
print(format_table_colums(columns))
print(format_table_colums(("---" for _ in columns)))
total_star_count = 0
for year in range(2015, 2021+1):
    year_star_count = 0
    for day in range(1, 25+1):
        day_date, day_puzzle_url, day_input_url, day_puzzle_file, day_input_file, day_python_file, day_rust_file = (
            v.format(year=year, day=day) for v in (date, puzzle_url, input_url, puzzle_file, input_file, python_file, rust_file))
        day_star_count = file_count_lines(day_puzzle_file, "<p>Your puzzle answer was <code>")
        day_puzzle_file, day_input_file, day_python_file, day_rust_file = (
            format_file(f) for f in (day_puzzle_file, day_input_file, day_python_file, day_rust_file))

        cols = [
            day_date,
            day_puzzle_url + " " + day_input_url,
            day_puzzle_file + " " + day_input_file,
            "*" * day_star_count,
            day_python_file,
            day_rust_file
        ]
        print(format_table_colums(cols))
        year_star_count += day_star_count
    print(format_table_colums((str(year_star_count) if c == "Stars" else "-" for c in columns)))
    total_star_count += year_star_count
print(format_table_colums((str(total_star_count) if c == "Stars" else "-" for c in columns)))

