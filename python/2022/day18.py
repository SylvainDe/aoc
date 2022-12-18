# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_cube_from_line(string):
    return tuple(int(s) for s in string.split(","))

def get_cubes_from_lines(string):
    return [get_cube_from_line(l) for l in string.splitlines()]

def get_cubes_from_file(file_path="../../resources/year2022_day18_input.txt"):
    with open(file_path) as f:
        return get_cubes_from_lines(f.read())


def get_surface_area(cubes):
    cubes = set(cubes)
    surface = 6 * len(cubes)
    for (x, y, z) in cubes:
        for (dx, dy, dz) in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
            if (x+dx, y+dy, z+dz) in cubes:
                surface -= 2
    return surface

def run_tests():
    cubes = get_cubes_from_lines("""1,1,1
    2,1,1""")
    assert get_surface_area(cubes) == 10

    cubes = get_cubes_from_lines("""2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5""")
    assert get_surface_area(cubes) == 64


def get_solutions():
    cubes = get_cubes_from_file()
    print(get_surface_area(cubes) == 3586)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
