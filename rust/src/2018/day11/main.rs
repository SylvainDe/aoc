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
    digit - 5
}

fn part1(serial: InputContent) -> (usize, usize) {
    // TODO: Use sliding windows for more efficiency
    let mut scores = Vec::new();
    for x in 1..=300 {
        for y in 1..=300 {
            let s: Int = (0..9)
                .map(|n| get_power_level(x + n % 3, y + n / 3, serial))
                .sum();
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
