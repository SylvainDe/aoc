# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_plot_from_lines(string):
    return {
        (i, j): v for i, l in enumerate(string.splitlines()) for j, v in enumerate(l)
    }


def get_plot_from_file(file_path=top_dir + "resources/year2024_day12_input.txt"):
    with open(file_path) as f:
        return get_plot_from_lines(f.read())


def get_neighbours(pos):
    x, y = pos
    yield x, y + 1
    yield x, y - 1
    yield x + 1, y
    yield x - 1, y


def get_regions(plot):
    plot = dict(plot)
    while plot:
        region = set()
        pos, val = plot.popitem()
        to_add = set([pos])
        while to_add:
            new = to_add.pop()
            if new not in region:
                region.add(new)
                for n in get_neighbours(new):
                    if plot.get(n, None) == val:
                        to_add.add(n)
                        plot.pop(n)
        yield region


def get_area(region):
    return len(region)


def get_perimeter(region):
    return sum(n not in region for p in region for n in get_neighbours(p))


def get_nb_seq(lst):
    nb = 1 if lst else 0
    for a, b in zip(lst, lst[1:]):
        if a + 1 != b:
            nb += 1
    return nb


def get_nb_sides(region):
    # To be optimised/simplified
    total_nb_sides = 0
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        sides = set((x, y) for x, y in region if (x + dx, y + dy) not in region)
        if dx == 0:
            distinct_ys = set(y for x, y in sides)
            nb_sides = sum(
                get_nb_seq(sorted(x for x, y in sides if y == y2)) for y2 in distinct_ys
            )
        else:
            distinct_xs = set(x for x, y in sides)
            nb_sides = sum(
                get_nb_seq(sorted(y for x, y in sides if x == x2)) for x2 in distinct_xs
            )
        total_nb_sides += nb_sides
    return total_nb_sides


def get_region_fencing_price(region, part2):
    return get_area(region) * (get_nb_sides(region) if part2 else get_perimeter(region))


def get_total_fencing_price(plot, part2=False):
    return sum(get_region_fencing_price(r, part2) for r in get_regions(plot))


def run_tests():
    plot = get_plot_from_lines(
        """AAAA
BBCD
BBCC
EEEC"""
    )
    assert get_total_fencing_price(plot) == 140
    assert get_total_fencing_price(plot, True) == 80

    plot = get_plot_from_lines(
        """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO"""
    )
    assert get_total_fencing_price(plot) == 772
    assert get_total_fencing_price(plot, True) == 436

    plot = get_plot_from_lines(
        """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""
    )
    assert get_total_fencing_price(plot) == 1930
    assert get_total_fencing_price(plot, True) == 1206


def get_solutions():
    plot = get_plot_from_file()
    print(get_total_fencing_price(plot) == 1352976)
    print(get_total_fencing_price(plot, True) == 808796)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
