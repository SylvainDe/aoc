use itertools::min;
use std::collections::HashSet;
use std::fs;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2018_day5_input.txt";

type Int = usize;
type InputContent = String;

fn get_input_from_str(string: &str) -> InputContent {
    let mut line_it = string.lines();
    line_it.next().unwrap().to_string()
}

fn get_input_from_file(filepath: &str) -> InputContent {
    get_input_from_str(&fs::read_to_string(filepath).expect("Could not open file"))
}

fn reduce(string: &InputContent) -> String {
    let mut reactors = HashSet::<(char, char)>::new();
    // Compute pairs
    for low in "abcdefghijklmnopqrstuvwxyz".chars() {
        let up = low.to_ascii_uppercase();
        reactors.insert((low, up));
        reactors.insert((up, low));
    }
    // Iterate and remove pairs as we go
    let mut accu = String::new();
    for c in string.chars() {
        if let Some(prev) = accu.pop() {
            if reactors.contains(&(c, prev)) {
                continue;
            }
            accu.push(prev);
        }
        accu.push(c);
    }
    accu
}

fn part1(string: &InputContent) -> Int {
    reduce(string).len()
}

fn part2(string: &InputContent) -> Int {
    // Not sure if it is smart but we first reduce the string before removing candidates pairs
    let s = reduce(string);
    // Remove and reduce
    min("abcdefghijklmnopqrstuvwxyz"
        .chars()
        .map(|low| reduce(&s.replace(low, "").replace(low.to_ascii_uppercase(), "")).len()))
    .unwrap()
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_file(INPUT_FILEPATH);
    let res = part1(&data);
    println!("{:?}", res);
    assert_eq!(res, 10638);
    let res2 = part2(&data);
    println!("{:?}", res2);
    assert_eq!(res2, 4944);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE: &str = "dabAcCaCBAcCcaDA
";

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE)), 10);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 4);
    }
}
