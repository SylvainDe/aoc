use common::input::get_first_line_from_file;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2018_day11_input.txt";

type Int = i32;
type InputContent = usize;

fn get_input_from_str(string: &str) -> InputContent {
    string.parse().unwrap()
}

fn get_input_from_file(filepath: &str) -> InputContent {
    get_input_from_str(&get_first_line_from_file(filepath))
}

fn get_power_level(x: usize, y: usize, serial: InputContent) -> Int {
    let rack_id = x + 10;
    let power = (rack_id * y + serial) * rack_id;
    let digit: Int = ((power / 100) % 10).try_into().unwrap();
    let ret = digit - 5;
    assert!((-5..5).contains(&ret));
    ret
}

/*
From the original grid, a cumulative grid can be computed.

          x                  x
   +------+---+       +------+---+
   |      |   |       |######|   |
 y +------+   |     y +------+   |
   |          |       |          |
   |          |       |          |
   +----------+       +----------+
     g(x,y)          c(x,y) = g(0, 0) + ... + g(x, 0)
                            + g(0, 1) + ... + g(x, 1)
                            +           ...
                            + g(0, y) + ... + g(x, y)

Then, the sum on an arbitrary sub-grid can be computed:
        x1   x2
    +----+---+-+
    |          |
    |          |
 y1 +    +---+ |
    |    |###| |
 y2 +    +---+ |
    |          |
    |          |
    +----------+

  sum(g(x,y) for x,y on the surface) is

        x1   x2          x1   x2          x1   x2          x1   x2
    +----+---+-+     +----+---+-+     +----+---+-+     +----+---+-+
    |########| |     |########| |     |###|      |     |###|      |
    |########| |     |--------+ |     |###|      |     |---+      |
 y1 +####+---+ |     +          |     +###|      |     +          |
    |####|###| |  -  |          |  -  |###|      |  +  |          |
 y2 +----+---+ |     +          |     +---+      |     +          |
    |          |     |          |     |          |     |          |
    |          |     |          |     |          |     |          |
    +----------+     +----------+     +----------+     +----------+

      c(x2,y2)    -  c(x2,y1-1)    -  c(x1-1,y2)    +  c(x1-1,y1-1)

Then each contribution is either counted:
 - (1-0-0+0) = 1 time for a point in the sub-grid
 - (1-1-1+1) = 0 time for a point in the upper-left corner
 - (1-1-0+0) = 0 time for a point in the left corner or upper corner

This principle can be used to compute the values in the cumulative grid:

   c(x,y) = g(x,y) + c(x,y-1) + c(x-1,y) - c(x-1,y-1)
 */

fn get_max_square(serial: InputContent, square_size: usize) -> (Int, usize, usize) {
    const X_MAX: usize = 300;
    const Y_MAX: usize = 300;

    // Compute cumulative grid
    let mut cum: [[Int; Y_MAX + 1]; X_MAX + 1] = [[0; Y_MAX + 1]; X_MAX + 1];
    for x in 1..=X_MAX {
        for y in 1..=Y_MAX {
            let pow_x_y = get_power_level(x, y, serial);
            cum[x][y] = pow_x_y + cum[x - 1][y] + cum[x][y - 1] - cum[x - 1][y - 1];
        }
    }

    // Compute score for windows
    let mut scores = Vec::new();
    for x in 1..=(X_MAX - square_size + 1) {
        let (x1, x2) = (x - 1, x + square_size - 1);
        for y in 1..=(Y_MAX - square_size + 1) {
            let (y1, y2) = (y - 1, y + square_size - 1);
            let s = cum[x2][y2] + cum[x1][y1] - cum[x2][y1] - cum[x1][y2];
            scores.push((s, x, y));
        }
    }
    *scores.iter().max().unwrap()
}

fn get_max_square2(serial: InputContent) -> (Int, usize, usize, usize) {
    const X_MAX: usize = 300;
    const Y_MAX: usize = 300;

    // Compute cumulative grid
    let mut cum: [[Int; Y_MAX + 1]; X_MAX + 1] = [[0; Y_MAX + 1]; X_MAX + 1];
    for x in 1..=X_MAX {
        for y in 1..=Y_MAX {
            let pow_x_y = get_power_level(x, y, serial);
            cum[x][y] = pow_x_y + cum[x - 1][y] + cum[x][y - 1] - cum[x - 1][y - 1];
        }
    }

    // Compute score for windows
    let mut scores = Vec::new();
    for square_size in 1..=X_MAX {
        for x in 1..=(X_MAX - square_size + 1) {
            let (x1, x2) = (x - 1, x + square_size - 1);
            for y in 1..=(Y_MAX - square_size + 1) {
                let (y1, y2) = (y - 1, y + square_size - 1);
                let s = cum[x2][y2] + cum[x1][y1] - cum[x2][y1] - cum[x1][y2];
                scores.push((s, x, y, square_size));
            }
        }
    }
    *scores.iter().max().unwrap()
}

fn part1(serial: InputContent) -> (usize, usize) {
    let (_score, x, y) = get_max_square(serial, 3);
    (x, y)
}

fn part2(serial: InputContent) -> (usize, usize, usize) {
    let (_score, x, y, size) = get_max_square2(serial);
    (x, y, size)
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_file(INPUT_FILEPATH);
    let res = part1(data);
    println!("{:?}", res);
    assert_eq!(res, (21, 68));
    let res2 = part2(data);
    println!("{:?}", res2);
    assert_eq!(res2, (90, 201, 15));
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;
    const SKIP_SLOW: bool = true;

    #[test]
    fn test_power_level() {
        assert_eq!(get_power_level(3, 5, 8), 4);
        assert_eq!(get_power_level(122, 79, 57), -5);
        assert_eq!(get_power_level(217, 196, 39), 0);
        assert_eq!(get_power_level(101, 153, 71), 4);
    }

    #[test]
    fn test_get_max_square() {
        assert_eq!(get_max_square(18, 3), (29, 33, 45));
        assert_eq!(get_max_square(42, 3), (30, 21, 61));
        assert_eq!(part1(18), (33, 45));
        assert_eq!(part1(42), (21, 61));
        assert_eq!(get_max_square(18, 16), (113, 90, 269));
        assert_eq!(get_max_square(42, 12), (119, 232, 251));
        if !SKIP_SLOW {
            assert_eq!(get_max_square2(18), (113, 90, 269, 16));
            assert_eq!(get_max_square2(42), (119, 232, 251, 12));
            assert_eq!(part2(18), (90, 269, 16));
            assert_eq!(part2(42), (232, 251, 12));
        }
    }
}
