# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_bingo_from_file(file_path="day4_input.txt"):
    with open(file_path) as f:
        lines = [l.strip() for l in f]
        numbers = [int(n) for n in lines[0].split(",")]
        grids = []
        grid = []
        for line in lines[1:]:
            if line:
                grid.append([int(n) for n in line.split()])
                grids.append(grid)
            else:
                grid = []
        return numbers, grids


def get_score(grid, numbers_seen, last_number):
    return sum(n for line in grid for n in line if n not in numbers_seen) * last_number


def play_bingo(bingo):
    numbers, grids = bingo
    numbers_seen = set()
    winning_grids = set()
    for number in numbers:
        numbers_seen.add(number)
        for gn, grid in enumerate(grids):
            if gn not in winning_grids:
                series = list(grid)
                for j in range(len(grid[0])):
                    series.append([line[j] for line in grid])
                for serie in series:
                    if all(n in numbers_seen for n in serie):
                        yield get_score(grid, numbers_seen, number)
                        winning_grids.add(gn)
                        break


def run_tests():
    bingo = get_bingo_from_file("day4_example_input.txt")
    bingo_scores = list(play_bingo(bingo))
    assert bingo_scores[0] == 4512
    assert bingo_scores[-1] == 1924


def get_solutions():
    bingo = get_bingo_from_file()
    bingo_scores = list(play_bingo(bingo))
    print(bingo_scores[0])
    print(bingo_scores[-1])


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
