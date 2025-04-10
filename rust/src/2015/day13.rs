// vi: set shiftwidth=4 tabstop=4 expandtab:
use common::input::check_answer;
use common::input::collect_from_lines;
use common::input::get_answers;
use common::input::get_file_content;
use core::str::FromStr;
use regex::Regex;
use std::sync::LazyLock;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2015_day13_input.txt";
const ANSWERS_FILEPATH: &str = "../resources/year2015_day13_answer.txt";

type Int = i32;

#[derive(Debug, PartialEq)]
struct HappinessCondition {
    name1: String,
    name2: String,
    nb: Int,
}

impl FromStr for HappinessCondition {
    type Err = ();
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        // Alice would gain 54 happiness units by sitting next to Bob.
        static RE: LazyLock<Regex> = LazyLock::new(|| {
            Regex::new(concat!(
                r"^(?P<name1>.*) would (?P<direction>gain|lose) (?P<nb>\d+) happiness units by sitting next to (?P<name2>.*)\.$"
        )).unwrap()
        });
        let c = RE.captures(s).ok_or(())?;
        let get_field = |s: &str| c.name(s).ok_or(());
        let direction = if get_field("direction")?.as_str() == "gain" {
            1
        } else {
            -1
        };
        Ok(Self {
            name1: get_field("name1")?.as_str().to_owned(),
            name2: get_field("name2")?.as_str().to_owned(),
            nb: direction * get_field("nb")?.as_str().parse::<Int>().map_err(|_| {})?,
        })
    }
}

type InputContent = Vec<HappinessCondition>;

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

    const EXAMPLE: &str = "Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.";

    #[test]
    fn test_foobar_from_str() {
        assert!(HappinessCondition::from_str("").is_err());
        assert_eq!(
            HappinessCondition::from_str(
                "Alice would gain 54 happiness units by sitting next to Bob."
            ),
            Ok(HappinessCondition {
                name1: "Alice".to_owned(),
                name2: "Bob".to_owned(),
                nb: 54
            })
        );
        assert_eq!(
            HappinessCondition::from_str(
                "Alice would lose 2 happiness units by sitting next to David."
            ),
            Ok(HappinessCondition {
                name1: "Alice".to_owned(),
                name2: "David".to_owned(),
                nb: -2
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
