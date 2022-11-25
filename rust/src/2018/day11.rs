use common::input::get_first_line_from_file;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2018_day11_input.txt";

type Int = i16;
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
 */

fn part1(serial: InputContent) -> (usize, usize) {
    // TODO: Use sliding windows for more efficiency
    const X_MAX: usize = 300;
    const Y_MAX: usize = 301;
    let mut pow: [[Int; Y_MAX + 1]; X_MAX + 1] = [[0; Y_MAX + 1]; X_MAX + 1];
    #[allow(clippy::needless_range_loop)]
    for x in 1..=X_MAX {
        for y in 1..=Y_MAX {
            pow[x][y] = get_power_level(x, y, serial);
        }
    }
    // let mut cum: [[Int; Y_MAX + 1]; X_MAX + 1] = [[0; Y_MAX + 1]; X_MAX + 1];
    // for x in 1..=X_MAX {
    //     for y in 1..=Y_MAX {
    //         cum[x][y] = pow[x][y] + cum[x-1][y] + cum[x][y-1];
    //     }
    // }

    let mut scores = Vec::new();
    for x in 1..=(X_MAX - 2) {
        for y in 1..=(Y_MAX - 2) {
            let s = pow[x][y]
                + pow[x][y + 1]
                + pow[x][y + 2]
                + pow[x + 1][y]
                + pow[x + 1][y + 1]
                + pow[x + 1][y + 2]
                + pow[x + 2][y]
                + pow[x + 2][y + 1]
                + pow[x + 2][y + 2];
            scores.push((s, x, y));
        }
    }
    let (_score, x, y) = scores.iter().max().unwrap();
    (*x, *y)
}

#[allow(clippy::missing_const_for_fn)]
fn part2(_arg: InputContent) -> Int {
    0
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_file(INPUT_FILEPATH);
    let res = part1(data);
    println!("{:?}", res);
    assert_eq!(res, (21, 68));
    let res2 = part2(data);
    println!("{:?}", res2);
    assert_eq!(res2, 0);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE: &str = "18";

    #[test]
    fn test_power_level() {
        assert_eq!(get_power_level(3, 5, 8), 4);
        assert_eq!(get_power_level(122, 79, 57), -5);
        assert_eq!(get_power_level(217, 196, 39), 0);
        assert_eq!(get_power_level(101, 153, 71), 4);
    }

    #[test]
    fn test_part1() {
        assert_eq!(part1(18), (33, 45));
        assert_eq!(part1(42), (21, 61));
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(get_input_from_str(EXAMPLE)), 0);
    }
}
