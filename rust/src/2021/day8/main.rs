use common::get_file_content;
use core::str::FromStr;
use std::borrow::ToOwned;
use std::collections::HashMap;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2021_day8_input.txt";

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
        Ok(Self {
            signals: p1.split(' ').map(ToOwned::to_owned).collect(),
            output: p2.split(' ').map(ToOwned::to_owned).collect(),
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
    get_input_from_str(&get_file_content(filepath))
}

const RAW_SEGMENTS: [[bool; 7]; 10] = [
    [true, true, true, false, true, true, true],
    [false, false, true, false, false, true, false],
    [true, false, true, true, true, false, true],
    [true, false, true, true, false, true, true],
    [false, true, true, true, false, true, false],
    [true, true, false, true, false, true, true],
    [true, true, false, true, true, true, true],
    [true, false, true, false, false, true, false],
    [true, true, true, true, true, true, true],
    [true, true, true, true, false, true, true],
];

fn part1(entries: &InputContent) -> usize {
    let mut seg_count = HashMap::<usize, usize>::new();
    for segments in RAW_SEGMENTS {
        let count = seg_count
            .entry(segments.iter().filter(|v| **v).count())
            .or_insert(0);
        *count += 1;
    }
    entries
        .iter()
        .map(|entry| {
            entry
                .output
                .iter()
                .filter(|s| seg_count.get(&s.len()) == Some(&1))
                .count()
        })
        .sum()
}

#[allow(clippy::trivially_copy_pass_by_ref, clippy::missing_const_for_fn)]
fn solve(_entry: &Entry) -> Int {
    0
}

fn part2(entries: &InputContent) -> Int {
    entries.iter().map(solve).sum()
}

fn main() {
    let before = Instant::now();
    let entries = get_input_from_file(INPUT_FILEPATH);
    let res = part1(&entries);
    println!("{:?}", res);
    assert_eq!(res, 449);
    let res2 = part2(&entries);
    println!("{:?}", res2);
    assert_eq!(res2, 0);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE: &str =
        "be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce";

    #[test]
    fn test_entry_from_str() {
        assert_eq!(Entry::from_str("acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"), Ok(Entry { signals: ["acedgfb", "cdfbe", "gcdfa", "fbcad", "dab", "cefabd", "cdfgeb", "eafb", "cagedb", "ab"].map(|s| s.to_owned()).to_vec(), output: ["cdfeb", "fcadb", "cdfeb", "cdbaf"].map(|s| s.to_owned()).to_vec() }));
    }

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE)), 26);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 0);
    }
}
