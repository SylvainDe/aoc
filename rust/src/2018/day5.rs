// vi: set shiftwidth=4 tabstop=4 expandtab:
use common::input::get_first_line_from_file;
use itertools::min;
use std::collections::HashSet;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2018_day5_input.txt";

type Int = usize;

fn reduce(string: &str) -> String {
    let mut reactors = HashSet::new();
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

fn part1(string: &str) -> Int {
    reduce(string).len()
}

fn part2(string: &str) -> Int {
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
    let data = get_first_line_from_file(INPUT_FILEPATH);
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

    const EXAMPLE: &str = "dabAcCaCBAcCcaDA";

    #[test]
    fn test_part1() {
        assert_eq!(part1(EXAMPLE), 10);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), 4);
    }
}
