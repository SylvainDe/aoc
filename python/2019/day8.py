# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import itertools


def get_image_from_file(file_path="../../resources/year2019_day8_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f][0]


def grouper(iterable, n, fillvalue=None):
    "Collect data into non-overlapping fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)


def get_layers(image, width, height):
    dim = width * height
    return grouper(image, dim)


def find_number1(image, width, height):
    layers = list(get_layers(image, width, height))
    layer = min(layers, key=lambda s: s.count("0"))
    return layer.count("1") * layer.count("2")


def get_pixel(index, layers):
    transparent = "2"
    for l in layers:
        v = l[index]
        if v != transparent:
            return v
    assert False


def get_image(image, width, height):
    layers = list(get_layers(image, width, height))
    pixels = "".join(get_pixel(i, layers) for i in range(len(layers[0])))
    return "\n".join("".join(line) for line in grouper(pixels, width))


def run_tests():
    image = "0222112222120000"
    assert get_image(image, 2, 2) == """01
10"""


def get_solutions():
    image = get_image_from_file()
    width, height = 25, 6
    print(find_number1(image, width, height))
    print(get_image(image, width, height).replace("0", " "))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
