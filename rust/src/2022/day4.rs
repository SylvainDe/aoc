// vi: set shiftwidth=4 tabstop=4 expandtab:
use common::input::collect_from_lines;
use common::input::get_file_content;
use core::str::FromStr;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2022_day4_input.txt";

type Int = u32;
#[derive(Debug, PartialEq)]
struct Identiers {
    id1_beg: Int,
    id1_end: Int,
    id2_beg: Int,
    id2_end: Int,
}
type InputContent = Vec<Identiers>;

impl FromStr for Identiers {
    type Err = ();
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let (id1, id2) = s.split_once(',').ok_or(())?;
        let (id1_beg, id1_end) = id1.split_once('-').ok_or(())?;
        let (id2_beg, id2_end) = id2.split_once('-').ok_or(())?;
        Ok(Self {
            id1_beg: id1_beg.parse().map_err(|_| {})?,
            id1_end: id1_end.parse().map_err(|_| {})?,
            id2_beg: id2_beg.parse().map_err(|_| {})?,
            id2_end: id2_end.parse().map_err(|_| {})?,
        })
    }
}

fn get_input_from_str(string: &str) -> InputContent {
    collect_from_lines(string)
}

fn part1(identifiers: &InputContent) -> Int {
    identifiers
        .iter()
        .map(
            |Identiers {
                 id1_beg,
                 id1_end,
                 id2_beg,
                 id2_end,
             }| {
                if (id1_beg <= id2_beg && id2_end <= id1_end)
                    || (id2_beg <= id1_beg && id1_end <= id2_end)
                {
                    1
                } else {
                    0
                }
            },
        )
        .sum()
}

fn part2(identifiers: &InputContent) -> Int {
    identifiers
        .iter()
        .map(
            |Identiers {
                 id1_beg,
                 id1_end,
                 id2_beg,
                 id2_end,
             }| {
                if (id1_beg > id2_end) || (id2_beg > id1_end) {
                    0
                } else {
                    1
                }
            },
        )
        .sum()
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_str(&get_file_content(INPUT_FILEPATH));
    let res = part1(&data);
    println!("{:?}", res);
    assert_eq!(res, 518);
    let res2 = part2(&data);
    println!("{:?}", res2);
    assert_eq!(res2, 909);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE: &str = "2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8";

    #[test]
    fn test_identifiers_from_str() {
        assert!(Identiers::from_str("").is_err());
        assert_eq!(
            Identiers::from_str("2-4,6-8"),
            Ok(Identiers {
                id1_beg: 2,
                id1_end: 4,
                id2_beg: 6,
                id2_end: 8
            })
        );
    }

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE)), 2);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 4);
    }
}
