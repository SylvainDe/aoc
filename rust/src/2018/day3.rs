// vi: set shiftwidth=4 tabstop=4 expandtab:
use common::input::check_answer;
use common::input::collect_from_lines;
use common::input::get_answers;
use common::input::get_file_content;
use core::str::FromStr;
use itertools::iproduct;
use regex::Regex;
use std::collections::HashMap;
use std::sync::LazyLock;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2018_day3_input.txt";
const ANSWERS_FILEPATH: &str = "../resources/year2018_day3_answer.txt";

type Int = u32;

#[derive(Debug, PartialEq)]
struct Claim {
    id: Int,
    leftedge: Int,
    topedge: Int,
    width: Int,
    height: Int,
}

impl FromStr for Claim {
    type Err = ();
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        // #20 @ 291,420: 12x21
        static RE: LazyLock<Regex> = LazyLock::new(|| {
            Regex::new(concat!(
                r"^#(?P<claimid>\d+) @ (?P<leftedge>\d+),(?P<topedge>\d+): (?P<width>\d+)x(?P<height>\d+)$"
        )).unwrap()
        });
        let c = RE.captures(s).ok_or(())?;
        let to_int = |s: &str| c.name(s).ok_or(())?.as_str().parse::<Int>().map_err(|_| {});
        Ok(Self {
            id: to_int("claimid")?,
            leftedge: to_int("leftedge")?,
            topedge: to_int("topedge")?,
            width: to_int("width")?,
            height: to_int("height")?,
        })
    }
}

impl Claim {
    fn fabric(&self) -> Vec<(Int, Int)> {
        iproduct!(
            self.topedge..self.topedge + self.height,
            self.leftedge..self.leftedge + self.width
        )
        .collect()
    }
}

type InputContent = Vec<Claim>;

fn get_input_from_str(string: &str) -> InputContent {
    collect_from_lines(string)
}

fn fabric_counter(claims: &InputContent) -> HashMap<(Int, Int), Int> {
    let mut counter = HashMap::new();
    for claim in claims {
        for p in claim.fabric() {
            let count = counter.entry(p).or_insert(0);
            *count += 1;
        }
    }
    counter
}

fn part1(claims: &InputContent) -> usize {
    fabric_counter(claims)
        .iter()
        .filter(|(_, &v)| v > 1)
        .count()
}

fn part2(claims: &InputContent) -> Int {
    let counter = fabric_counter(claims);
    for claim in claims {
        if claim
            .fabric()
            .iter()
            .all(|&p| *counter.get(&p).expect("Point in counter") == 1)
        {
            return claim.id;
        }
    }
    0
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_str(&get_file_content(INPUT_FILEPATH));
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

    const EXAMPLE: &str = "#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2";

    #[test]
    fn test_claim_from_str() {
        assert!(Claim::from_str("").is_err());
        assert_eq!(
            Claim::from_str("#123 @ 3,2: 5x4"),
            Ok(Claim {
                id: 123,
                leftedge: 3,
                topedge: 2,
                width: 5,
                height: 4,
            })
        );
    }

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE)), 4);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 3);
    }
}
