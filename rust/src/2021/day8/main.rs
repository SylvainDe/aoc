use core::str::FromStr;
use std::borrow::ToOwned;
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
    get_input_from_str(&fs::read_to_string(filepath).expect("Could not open file"))
}

fn part1(entries: &InputContent) -> usize {
    entries
        .iter()
        .map(|entry| {
            entry
                .output
                .iter()
                .filter(|s| [2, 3, 4, 7].contains(&s.len()))
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
    let entries = get_input_from_file(INPUT_FILEPATH);
    let res = part1(&entries);
    println!("{:?}", res);
    assert_eq!(res, 449);
    let res2 = part2(&entries);
    println!("{:?}", res2);
    assert_eq!(res2, 0);
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
