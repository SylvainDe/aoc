use common::collect_from_lines;
use common::get_file_content;
use core::str::FromStr;
use lazy_static::lazy_static;
use regex::Captures;
use regex::Regex;
use std::collections::HashMap;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2018_day3_input.txt";

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
        lazy_static! {
        static ref RE: Regex =
            Regex::new(r"^#(?P<claimid>\d+) @ (?P<leftedge>\d+),(?P<topedge>\d+): (?P<width>\d+)x(?P<height>\d+)$")
                .unwrap();
        }
        let c = RE.captures(s).ok_or(())?;
        let to_int =
            |c: &Captures, s: &str| c.name(s).ok_or(())?.as_str().parse::<Int>().map_err(|_| {});
        Ok(Self {
            id: to_int(&c, "claimid")?,
            leftedge: to_int(&c, "leftedge")?,
            topedge: to_int(&c, "topedge")?,
            width: to_int(&c, "width")?,
            height: to_int(&c, "height")?,
        })
    }
}

impl Claim {
    fn fabric(&self) -> Vec<(Int, Int)> {
        let mut v = Vec::<(Int, Int)>::new();
        for x in self.topedge..self.topedge + self.height {
            for y in self.leftedge..self.leftedge + self.width {
                v.push((x, y));
            }
        }
        v
    }
}

type InputContent = Vec<Claim>;

fn get_input_from_str(string: &str) -> InputContent {
    collect_from_lines(string, Claim::from_str)
}

fn get_input_from_file(filepath: &str) -> InputContent {
    get_input_from_str(&get_file_content(filepath))
}

fn part1(claims: &InputContent) -> usize {
    let mut counter = HashMap::<(Int, Int), Int>::new();
    for claim in claims {
        for p in claim.fabric() {
            let count = counter.entry(p).or_insert(0);
            *count += 1;
        }
    }
    counter.iter().filter(|(_, &v)| v > 1).count()
}

#[allow(clippy::missing_const_for_fn)]
fn part2(_arg: &InputContent) -> Int {
    0
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_file(INPUT_FILEPATH);
    let res = part1(&data);
    println!("{:?}", res);
    assert_eq!(res, 109_716);
    let res2 = part2(&data);
    println!("{:?}", res2);
    assert_eq!(res2, 0);
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
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 0);
    }
}
