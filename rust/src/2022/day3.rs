// vi: set shiftwidth=4 tabstop=4 expandtab:
use common::input::check_answer;
use common::input::collect_lines;
use common::input::get_answers;
use common::input::get_file_content;
use std::collections::HashSet;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2022_day3_input.txt";
const ANSWERS_FILEPATH: &str = "../resources/year2022_day3_answer.txt";

type Int = u32;
type InputContent = Vec<String>;

fn get_input_from_str(string: &str) -> InputContent {
    collect_lines(string)
}

fn get_char_prio(c: char) -> Int {
    if c.is_lowercase() {
        (c as Int) - ('a' as Int) + 1
    } else if c.is_uppercase() {
        (c as Int) - ('A' as Int) + 27
    } else {
        panic!("Unexpected char");
    }
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
    get_char_prio(*item)
}

fn part1(rucksacks: &InputContent) -> Int {
    rucksacks.iter().map(double_compartment_priority).sum()
}

fn badge_prio(s1: &str, s2: &str, s3: &str) -> Int {
    let s1 = s1.chars().collect::<HashSet<char>>();
    let s2 = s2.chars().collect::<HashSet<char>>();
    let s3 = s3.chars().collect::<HashSet<char>>();
    let intersect = s1.intersection(&s2).copied().collect::<HashSet<char>>();
    let intersect = s3
        .intersection(&intersect)
        .copied()
        .collect::<HashSet<char>>();
    let item = intersect.iter().next().unwrap();
    get_char_prio(*item)
}

fn part2(rucksacks: &InputContent) -> Int {
    rucksacks
        .chunks(3)
        .map(|s| badge_prio(&s[0], &s[1], &s[2]))
        .sum()
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

    const EXAMPLE: &str = "";

    #[test]
    const fn test_double_compartment_priority() {
        // TODO
    }

    #[test]
    const fn test_badge_priority() {
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
