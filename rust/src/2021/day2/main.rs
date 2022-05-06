use core::str::FromStr;
use std::fs::File;
use std::io::BufRead;
use std::io::BufReader;

const INPUT_FILEPATH: &str = "res/2021/day2/input.txt";

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
            "forward" => Ok(Action::Forward),
            "down" => Ok(Action::Down),
            "up" => Ok(Action::Up),
            _ => Err(()),
        }
    }
}

#[derive(Debug, PartialEq)]
struct Command {
    action: Action,
    value: u32,
}

impl FromStr for Command {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let (action, value) = s.split_once(' ').ok_or(())?;
        Ok(Command {
            action: Action::from_str(action)?,
            value: value.parse().map_err(|_| {})?,
        })
    }
}

fn get_input_from_file(filepath: &str) -> Vec<Command> {
    BufReader::new(File::open(filepath).expect("Could not open file"))
        .lines()
        .map(|line| Command::from_str(&line.unwrap()).unwrap())
        .collect()
}

fn part1(commands: Vec<Command>) -> i32 {
    let (mut depth, mut position): (i32, i32) = (0, 0);
    for Command { action, value } in commands {
        match action {
            Action::Forward => position += value as i32,
            Action::Down => depth += value as i32,
            Action::Up => depth -= value as i32,
        }
    }
    depth * position
}

fn main() {
    println!("Hello, world!");
    let commands = get_input_from_file(INPUT_FILEPATH);
    println!("{:?}", part1(commands));
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
        assert!(Command::from_str("up -3").is_err());
        assert!(Command::from_str("backward 2").is_err());
    }

    const EXAMPLE: &str = "forward 5
down 5
forward 8
up 3
down 8
forward 2";

    fn get_input_from_str(s: &str) -> Vec<Command> {
        s.split('\n')
            .map(|line| Command::from_str(line).unwrap())
            .collect()
    }

    #[test]
    fn test_part1() {
        assert_eq!(part1(get_input_from_str(EXAMPLE)), 150);
    }
}
