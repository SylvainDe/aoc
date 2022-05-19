use itertools::min;
use itertools::Itertools;
use std::collections::HashSet;
use std::fs;

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
    // Remove pairs
    let mut string = string.clone();
    'outer: loop {
        for (prev, next) in string.chars().tuple_windows() {
            if reactors.contains(&(prev, next)) {
                // Not very suble nor very elegant
                let sub = prev.to_string() + &next.to_string();
                string = string.replace(&sub, "");
                continue 'outer;
            }
        }
        return string;
    }
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
    let data = get_input_from_file(INPUT_FILEPATH);
    let res = part1(&data);
    println!("{:?}", res);
    assert_eq!(res, 10638);
    let res2 = part2(&data);
    println!("{:?}", res2);
    assert_eq!(res2, 4944);
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
