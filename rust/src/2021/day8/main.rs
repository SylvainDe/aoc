use core::str::FromStr;
use std::fs;

const INPUT_FILEPATH: &str = "res/2021/day8/input.txt";

type Int = u32;

#[derive(Debug, PartialEq)]
struct Entry {
    signals: Vec<String>,
    output: Vec<String>,
}

impl FromStr for Entry {
    type Err = ();
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let (p1, p2) = s.split_once(" | ").ok_or(())?;
        Ok(Entry {
            signals: p1.split(' ').map(|s| s.to_owned()).collect(),
            output: p2.split(' ').map(|s| s.to_owned()).collect(),
        })
    }
}

type InputContent = Vec<Entry>;

fn get_input_from_str(string: &str) -> InputContent {
    string
        .lines()
        .map(|line| Entry::from_str(line).unwrap())
        .collect()
}

fn get_input_from_file(filepath: &str) -> InputContent {
    get_input_from_str(&fs::read_to_string(filepath).expect("Could not open file"))
}

fn part1(_arg: &InputContent) -> Int {
    0
}

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

    const EXAMPLE: &str = "";

    #[test]
    fn test_entry_from_str() {
        assert_eq!(Entry::from_str("acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"), Ok(Entry { signals: ["acedgfb", "cdfbe", "gcdfa", "fbcad", "dab", "cefabd", "cdfgeb", "eafb", "cagedb", "ab"].map(|s| s.to_owned()).to_vec(), output: ["cdfeb", "fcadb", "cdfeb", "cdbaf"].map(|s| s.to_owned()).to_vec() }));
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
