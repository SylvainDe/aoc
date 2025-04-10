// vi: set shiftwidth=4 tabstop=4 expandtab:
use common::input::check_answer;
use common::input::collect_from_lines;
use common::input::get_answers;
use common::input::get_file_content;
use core::str::FromStr;
use regex::Regex;
use std::sync::LazyLock;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/yearYYYY_dayDD_input.txt";
const ANSWERS_FILEPATH: &str = "../resources/yearYYYY_dayDD_answer.txt";

type Int = u32;

#[derive(Debug, PartialEq)]
struct FooBar {
    char1: char,
    int2: Int,
}

impl FromStr for FooBar {
    type Err = ();
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        // TODO: Example of the regexp
        static RE: LazyLock<Regex> =
            LazyLock::new(|| Regex::new(concat!(r"^(?P<char1>.) (?P<int2>\d+)$")).unwrap());
        let c = RE.captures(s).ok_or(())?;
        Ok(Self {
            char1: c
                .name("char1")
                .ok_or(())?
                .as_str()
                .chars()
                .next()
                .ok_or(())?,
            int2: c
                .name("int2")
                .ok_or(())?
                .as_str()
                .parse::<Int>()
                .map_err(|_| {})?,
        })
    }
}

type InputContent = Vec<FooBar>;

fn get_input_from_str(string: &str) -> InputContent {
    collect_from_lines(string)
}

#[expect(clippy::missing_const_for_fn, reason = "Not implemented yet")]
fn part1(_arg: &InputContent) -> Int {
    0
}

#[expect(clippy::missing_const_for_fn, reason = "Not implemented yet")]
fn part2(_arg: &InputContent) -> Int {
    0
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_str(&get_file_content(INPUT_FILEPATH));
    let (ans, ans2) = get_answers(ANSWERS_FILEPATH);
    let solved = false;
    let res = part1(&data);
    check_answer(&res.to_string(), ans, solved);
    let res2 = part2(&data);
    check_answer(&res2.to_string(), ans2, solved);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE: &str = "C 1
C 2
A 3";

    #[test]
    fn test_foobar_from_str() {
        assert!(FooBar::from_str("").is_err());
        assert_eq!(
            FooBar::from_str("C 42"),
            Ok(FooBar {
                char1: 'C',
                int2: 42
            })
        );
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
