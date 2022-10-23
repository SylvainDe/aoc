"""Script to generate README.

Usage: python3 generate_readme.py > README.md
"""
import os

# Separator
sep = "|"

# URLs
puzzle_url="[Problem](https://adventofcode.com/{year}/day/{day})"
input_url="[Input](https://adventofcode.com/{year}/day/{day}/input)"
urls = (puzzle_url, input_url)

# Local files
input_file="resources/year{year}_day{day}_input.txt"
python_file="python/{year}/day{day}.py"
rust_file="rust/src/{year}/day{day}/main.rs"
files = (input_file, python_file, rust_file)

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

def format_file(filepath):
    if not os.path.isfile(filepath):
        return ""
    basename=os.path.basename(filepath)
    note=""
    if basename.endswith(".py"):
        if file_contains(filepath, "xxx = get_xxx_from_file"):
            note = ": template"
    elif basename.endswith(".rs"):
        if file_contains(filepath, "fn part1(_arg"):
            note = ": template"
    return "[{basename}{note}]({fullpath})".format(basename=basename, note=note, fullpath=filepath)

def format_table_colums(columns):
    return "{}{}{}".format(sep, sep.join(columns), sep)

# Generation
print(header)
columns = ["Year", "Day", "Problem URL", "Input URL", "Input", "Python", "Rust"]
print(format_table_colums(columns))
print(format_table_colums(("---" for _ in columns)))
for year in range(2016, 2021+1):
    for day in range(1, 25+1):
        day_urls = [u.format(year=year, day=day) for u in urls]
        day_files = [format_file(f.format(year=year, day=day)) for f in files]
        columns = [str(year), str(day)] + day_urls + day_files
        print(format_table_colums(columns))
    print(format_table_colums(("-" for _ in columns)))

