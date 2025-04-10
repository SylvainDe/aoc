// vi: set shiftwidth=4 tabstop=4 expandtab:
use common::input::check_answer;
use common::input::get_answers;
use common::input::get_first_line_from_file;
use core::str::FromStr;
use std::collections::HashSet;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2016_day1_input.txt";
const ANSWERS_FILEPATH: &str = "../resources/year2016_day1_answer.txt";

type Int = i32;

#[derive(Debug, PartialEq)]
enum Turn {
    Left,
    Right,
}

impl FromStr for Turn {
    type Err = ();
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "L" => Ok(Self::Left),
            "R" => Ok(Self::Right),
            _ => Err(()),
        }
    }
}

#[derive(Debug, PartialEq)]
struct Action {
    turn: Turn,
    length: Int,
}

impl FromStr for Action {
    type Err = ();
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut char_it = s.chars();
        let first_char = char_it.next();
        match first_char {
            Some(c) => Ok(Self {
                turn: c.to_string().parse().map_err(|()| {})?,
                length: char_it.collect::<String>().parse().map_err(|_| {})?,
            }),
            None => Err(()),
        }
    }
}

type InputContent = Vec<Action>;

fn get_input_from_str(string: &str) -> InputContent {
    string
        .split(", ")
        .map(|s| s.parse::<Action>().unwrap())
        .collect()
}

// TODO: Define logic in https://doc.rust-lang.org/std/iter/fn.from_fn.html ?
fn part1(arg: &InputContent) -> Int {
    let mut x: Int = 0;
    let mut y: Int = 0;
    let mut dx: Int = 0;
    let mut dy: Int = 1;
    for Action { turn, length } in arg {
        match turn {
            Turn::Left => (dx, dy) = (-dy, dx),
            Turn::Right => (dx, dy) = (dy, -dx),
        }
        x += dx * length;
        y += dy * length;
    }
    x.abs() + y.abs()
}

fn part2(arg: &InputContent) -> Int {
    let mut x: Int = 0;
    let mut y: Int = 0;
    let mut dx: Int = 0;
    let mut dy: Int = 1;
    let mut positions = HashSet::new();
    positions.insert((x, y));
    for Action { turn, length } in arg {
        match turn {
            Turn::Left => (dx, dy) = (-dy, dx),
            Turn::Right => (dx, dy) = (dy, -dx),
        }
        for _i in 0..*length {
            x += dx;
            y += dy;
            if positions.contains(&(x, y)) {
                return x.abs() + y.abs();
            }
            positions.insert((x, y));
        }
    }
    0
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_str(&get_first_line_from_file(INPUT_FILEPATH));
    let (ans, ans2) = get_answers(ANSWERS_FILEPATH);
    let solved = true;
    let res = part1(&data);
    check_answer(&res.to_string(), ans, solved);
    let res2 = part2(&data);
    check_answer(&res2.to_string(), ans2, solved);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_action_from_str() {
        assert_eq!(
            Action::from_str("R5"),
            Ok(Action {
                turn: Turn::Right,
                length: 5
            })
        );
    }

    #[test]
    fn test_part1() {
        const EXAMPLE: &str = "R5, L5, R5, R3";
        assert_eq!(part1(&get_input_from_str(EXAMPLE)), 12);
    }

    #[test]
    fn test_part2() {
        const EXAMPLE: &str = "R8, R4, R4, R8";
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 4);
    }
}
