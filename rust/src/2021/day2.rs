use common::input::collect_from_lines;
use common::input::get_file_content;
use core::str::FromStr;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2021_day2_input.txt";

type Int = i32;

#[derive(Debug, PartialEq)]
enum Action {
    Forward,
    Down,
    Up,
}

impl FromStr for Action {
    type Err = ();
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "forward" => Ok(Self::Forward),
            "down" => Ok(Self::Down),
            "up" => Ok(Self::Up),
            _ => Err(()),
        }
    }
}

#[derive(Debug, PartialEq)]
struct Command {
    action: Action,
    value: Int,
}

impl FromStr for Command {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let (action, value) = s.split_once(' ').ok_or(())?;
        Ok(Self {
            action: Action::from_str(action)?,
            value: value.parse().map_err(|_| {})?,
        })
    }
}

type InputContent = Vec<Command>;

fn get_input_from_str(string: &str) -> InputContent {
    collect_from_lines(string)
}

fn part1(commands: &InputContent) -> Int {
    let (mut depth, mut position): (Int, Int) = (0, 0);
    for Command { action, value } in commands {
        match action {
            Action::Forward => position += value,
            Action::Down => depth += value,
            Action::Up => depth -= value,
        }
    }
    depth * position
}

fn part2(commands: &InputContent) -> Int {
    let (mut depth, mut position, mut aim): (Int, Int, Int) = (0, 0, 0);
    for Command { action, value } in commands {
        match action {
            Action::Forward => {
                position += value;
                depth += aim * value;
            }
            Action::Down => aim += value,
            Action::Up => aim -= value,
        }
    }
    depth * position
}

fn main() {
    let before = Instant::now();
    let commands = get_input_from_str(&get_file_content(INPUT_FILEPATH));
    let res = part1(&commands);
    println!("{:?}", res);
    assert_eq!(res, 1_670_340);
    let res2 = part2(&commands);
    println!("{:?}", res2);
    assert_eq!(res2, 1_954_293_920);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn action_from_str_valid() {
        assert_eq!(Action::from_str("forward"), Ok(Action::Forward));
        assert_eq!(Action::from_str("down"), Ok(Action::Down));
        assert_eq!(Action::from_str("up"), Ok(Action::Up));
    }

    #[test]
    fn action_from_str_invalid() {
        assert!(Action::from_str("backward").is_err());
    }

    #[test]
    fn command_from_str_valid() {
        assert_eq!(
            Command::from_str("forward 5"),
            Ok(Command {
                action: Action::Forward,
                value: 5
            })
        );
        assert_eq!(
            Command::from_str("down 2"),
            Ok(Command {
                action: Action::Down,
                value: 2
            })
        );
        assert_eq!(
            Command::from_str("up 3"),
            Ok(Command {
                action: Action::Up,
                value: 3
            })
        );
    }

    #[test]
    fn command_from_str_invalid_values() {
        assert!(Command::from_str("up three").is_err());
        assert!(Command::from_str("backward 2").is_err());
    }

    const EXAMPLE: &str = "forward 5
down 5
forward 8
up 3
down 8
forward 2";

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE)), 150);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 900);
    }
}
