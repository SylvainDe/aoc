use core::str::FromStr;
use std::fs;

const INPUT_FILEPATH: &str = "../resources/year2018_day6_input.txt";

type Int = i32;

#[derive(Debug, PartialEq, Eq, Hash)]
struct Point {
    x: Int,
    y: Int,
}

impl FromStr for Point {
    type Err = ();
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let (x, y) = s.split_once(", ").ok_or(())?;
        Ok(Self {
            x: x.parse().map_err(|_| {})?,
            y: y.parse().map_err(|_| {})?,
        })
    }
}

type InputContent = Vec<Point>;

fn get_input_from_str(string: &str) -> InputContent {
    string
        .lines()
        .map(|line| Point::from_str(line).unwrap())
        .collect()
}

fn get_input_from_file(filepath: &str) -> InputContent {
    get_input_from_str(&fs::read_to_string(filepath).expect("Could not open file"))
}

#[allow(clippy::trivially_copy_pass_by_ref, clippy::missing_const_for_fn)]
fn part1(_arg: &InputContent) -> Int {
    // TODO: First step - filter interior points and exterior points
    0
}

#[allow(clippy::trivially_copy_pass_by_ref, clippy::missing_const_for_fn)]
fn part2(_arg: &InputContent) -> Int {
    0
}

fn main() {
    let data = get_input_from_file(INPUT_FILEPATH);
    let res = part1(&data);
    println!("{:?}", res);
    assert_eq!(res, 0);
    let res2 = part2(&data);
    println!("{:?}", res2);
    assert_eq!(res2, 0);
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE: &str = "1, 1
1, 6
8, 3
3, 4
5, 5
8, 9";

    #[test]
    fn test_point_from_str() {
        assert_eq!(Point::from_str("9, 4"), Ok(Point { x: 9, y: 4 }));
    }

    #[test]
    fn point_from_str_invalid_values() {
        assert!(Point::from_str("9 4").is_err());
        assert!(Point::from_str("9,4").is_err());
        assert!(Point::from_str("9,four").is_err());
    }

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE)), 0);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 0);
    }
}
