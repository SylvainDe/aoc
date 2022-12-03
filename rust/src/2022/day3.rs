use common::input::collect_lines;
use common::input::get_file_content;
use std::collections::HashSet;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2022_day3_input.txt";

type Int = u32;
type InputContent = Vec<String>;

fn get_input_from_str(string: &str) -> InputContent {
    collect_lines(string)
}

fn double_compartment_priority(s: &String) -> Int {
    let len = s.len();
    assert_eq!(len % 2, 0);
    let half = len / 2;
    let (s1, s2) = s.split_at(half);
    assert_eq!(s1.len(), s2.len());
    let s1 = s1.chars().collect::<HashSet<char>>();
    let s2 = s2.chars().collect::<HashSet<char>>();
    let mut intersect = s1.intersection(&s2);
    let item = intersect.next().unwrap();
    if item.is_lowercase() {
        (*item as Int) - ('a' as Int) + 1
    } else if item.is_uppercase() {
        (*item as Int) - ('A' as Int) + 27
    } else {
        panic!("Unexpected char");
    }
}

fn part1(rucksacks: &InputContent) -> Int {
    rucksacks.iter().map(double_compartment_priority).sum()
}

#[allow(clippy::missing_const_for_fn)]
fn part2(_arg: &InputContent) -> Int {
    0
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_str(&get_file_content(INPUT_FILEPATH));
    let res = part1(&data);
    println!("{:?}", res);
    assert_eq!(res, 7889);
    let res2 = part2(&data);
    println!("{:?}", res2);
    assert_eq!(res2, 0);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE: &str = "";

    #[test]
    fn test_double_compartment_priority() {
        // TODO
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
