# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import math


def get_tiles_from_file(file_path="day20_input.txt"):
    with open(file_path) as f:
        return get_tiles_from_string(f.read())


def top(tile):
    return "".join(tile[0])


def bottom(tile):
    return "".join(tile[-1])


def left(tile):
    return "".join(line[0] for line in tile)


def right(tile):
    return "".join(line[-1] for line in tile)


def get_tile_borders(tile):
    return (
        top(tile),
        right(tile),
        bottom(tile),
        left(tile),
    )


def rotate(matrix):
    # https://stackoverflow.com/questions/8421337/rotating-a-two-dimensional-array-in-python
    return list(zip(*matrix[::-1]))


def get_rotations_and_symetries(tile):
    t = tile
    yield t
    for i in range(3):
        t = rotate(t)
        yield t
    t = t[::-1]
    yield t
    for i in range(3):
        t = rotate(t)
        yield t


def get_tile_from_string(string):
    lines = string.splitlines()
    number = int(lines[0][len("Tiles:") - 1 : -1])
    return number, lines[1:]


def get_tiles_from_string(string):
    tiles_dict = dict()
    for s in string.split("\n\n"):
        nb, cont = get_tile_from_string(s)
        tiles_dict[nb] = cont
    return tiles_dict


def guess_corners(tiles):
    tiles_borders = {k: get_tile_borders(v) for k, v in tiles.items()}
    sides = dict()
    for n, tile in tiles_borders.items():
        for side in tile:
            for s in (side, side[::-1]):
                sides.setdefault(s, []).append(n)
    unique_sides = set([s for s, lst in sides.items() if len(lst) == 1])
    corners = [
        n
        for n, tile in tiles_borders.items()
        if sum(side in unique_sides for side in tile) == 2
    ]
    assert len(corners) == 4
    return corners


def guess_image(tiles):
    tiles_borders = {k: get_tile_borders(v) for k, v in tiles.items()}
    sides = dict()
    for n, tile in tiles_borders.items():
        for side in tile:
            for s in (side, side[::-1]):
                sides.setdefault(s, []).append(n)

    unique_sides = set([s for s, lst in sides.items() if len(lst) == 1])

    # Determine corners and sides
    corners, borders, middles = [], [], []
    for n, tile in tiles_borders.items():
        nb_unique = sum(side in unique_sides for side in tile)
        if nb_unique == 2:
            corners.append(n)
        elif nb_unique == 1:
            borders.append(n)
        elif nb_unique == 0:
            middles.append(n)
        else:
            assert False

    # Check that what we have found makes sense
    nb_tiles = len(tiles)
    side_len = int(math.sqrt(nb_tiles))
    assert side_len * side_len == nb_tiles

    assert len(corners) == 4
    assert len(borders) + len(corners) == 4 * (side_len - 1)

    # Build image starting from a corner
    remaining_id = set(tiles)
    image = []
    for i in range(side_len):
        curr_line = []
        for j in range(side_len):
            n, tile = find_match_for_border(
                tiles,
                remaining_id if (i, j) != (0, 0) else [corners[0]],
                [right(curr_line[-1])] if j else unique_sides,
                [bottom(image[-1][j])] if i else unique_sides,
            )
            remaining_id.remove(n)
            curr_line.append(tile)
        image.append(curr_line)
    assert not remaining_id
    assert sum(len(line) for line in image) == nb_tiles

    return stitch_image(image)


def stitch_image(tiles):
    img = []
    for tile_line in tiles:
        line_no_border = [remove_borders(tile) for tile in tile_line]
        for i in range(len(line_no_border[0])):
            img.append("".join(t[i] for t in line_no_border))
    return img


def remove_borders(tile):
    return ["".join(line[1:-1]) for line in tile[1:-1]]


def find_match_for_border(tiles, candidates, lefts, ups):
    found = [
        (c, t)
        for c in candidates
        for t in get_rotations_and_symetries(tiles[c])
        if top(t) in ups and left(t) in lefts
    ]
    assert len(found) in (1, 2)
    assert len(set(f[0] for f in found)) == 1
    return found[0]


def get_caracter_positions(matrix, char):
    return set(
        (i, j) for i, line in enumerate(matrix) for j, c in enumerate(line) if c == char
    )


def water_roughness(monster, image):
    water_hashes = get_caracter_positions(image, "#")
    found_hashes = set()
    for m in get_rotations_and_symetries(monster):
        monster_hashes = get_caracter_positions(m, "#")
        for i in range(len(image)):
            for j in range(len(image)):
                positions = [(mx + i, my + j) for mx, my in monster_hashes]
                if all(pos in water_hashes for pos in positions):
                    found_hashes.update(positions)
    return len(water_hashes) - len(found_hashes)


def mult(iterator):
    m = 1
    for i in iterator:
        m *= i
    return m


monster = ["                  # ", "#    ##    ##    ###", " #  #  #  #  #  #   "]


def test_get_rotations_and_symetries():
    assert list(get_rotations_and_symetries([[1, 2], [3, 4]])) == [
        [[1, 2], [3, 4]],
        [(3, 1), (4, 2)],
        [(4, 3), (2, 1)],
        [(2, 4), (1, 3)],
        [(1, 3), (2, 4)],
        [(2, 1), (4, 3)],
        [(4, 2), (3, 1)],
        [(3, 4), (1, 2)],
    ]
    assert list(get_rotations_and_symetries([[1, 2, 3], [4, 5, 6], [7, 8, 9]])) == [
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        [(7, 4, 1), (8, 5, 2), (9, 6, 3)],
        [(9, 8, 7), (6, 5, 4), (3, 2, 1)],
        [(3, 6, 9), (2, 5, 8), (1, 4, 7)],
        [(1, 4, 7), (2, 5, 8), (3, 6, 9)],
        [(3, 2, 1), (6, 5, 4), (9, 8, 7)],
        [(9, 6, 3), (8, 5, 2), (7, 4, 1)],
        [(7, 8, 9), (4, 5, 6), (1, 2, 3)],
    ]


def run_tests():
    test_get_rotations_and_symetries()
    example1 = """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###..."""
    tiles = get_tiles_from_string(example1)
    assert mult(guess_corners(tiles)) == 20899048083289
    image1 = """.#.#..#.##...#.##..#####
###....#.#....#..#......
##.##.###.#.#..######...
###.#####...#.#####.#..#
##.#....#.##.####...#.##
...########.#....#####.#
....#..#...##..#.#.###..
.####...#..#.....#......
#..#.##..#..###.#.##....
#.####..#.####.#.#.###..
###.#.#...#.######.#..##
#.####....##..########.#
##..##.#...#...#.#.#.#..
...#..#..#.#.##..###.###
.#.#....#.##.#...###.##.
###.#...#..#.##.######..
.#.#.###.##.##.#..#.##..
.####.###.#...###.#..#.#
..#.#..#..#.#.#.####.###
#..####...#.#.#.###.###.
#####..#####...###....##
#.##..#..#...#..####...#
.#.###..##..##..####.##.
...###...##...#...#..###""".splitlines()
    image1_rot = list("".join(l) for l in zip(*image1))
    assert guess_image(tiles) in (image1, image1_rot)
    assert water_roughness(monster, image1) == 273
    assert water_roughness(monster, image1_rot) == 273


def get_solutions():
    tiles = get_tiles_from_file()
    print(mult(guess_corners(tiles)) == 140656720229539)
    image = guess_image(tiles)
    print(water_roughness(monster, image) == 1885)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
