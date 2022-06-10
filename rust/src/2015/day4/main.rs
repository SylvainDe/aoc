use common::get_first_line;
use std::fs;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2015_day4_input.txt";

type Int = u32;
type InputContent = String;
const SKIP_SLOW: bool = true;

fn get_input_from_str(string: &str) -> InputContent {
    get_first_line(string)
}

fn get_input_from_file(filepath: &str) -> InputContent {
    get_input_from_str(&fs::read_to_string(filepath).expect("Could not open file"))
}

fn digest_starts_with(data: &str, prefix: &str) -> bool {
    let digest = format!("{:?}", md5::compute(data));
    digest.starts_with(prefix)
}

fn find_coin(data: &str, prefix: &str) -> Int {
    for i in 0.. {
        let s = format!("{}{}", data, i);
        if digest_starts_with(&s, prefix) {
            return i;
        }
    }
    0
}

fn part1(input: &InputContent) -> Int {
    find_coin(input, "00000")
}

fn part2(input: &InputContent) -> Int {
    find_coin(input, "000000")
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_file(INPUT_FILEPATH);
    let res = part1(&data);
    println!("{:?}", res);
    assert_eq!(res, 282_749);
    if !SKIP_SLOW {
        let res2 = part2(&data);
        println!("{:?}", res2);
        assert_eq!(res2, 9_962_624);
    }
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_digest_starts_with() {
        assert!(digest_starts_with("abcdef609043", "00000"));
        assert!(!digest_starts_with("abcdef609043", "000000"));
    }

    #[test]
    fn test_find_coin() {
        assert_eq!(find_coin("abcdef", "00000"), 609_043);
        if !SKIP_SLOW {
            assert_eq!(find_coin("pqrstuv", "00000"), 1_048_970);
        }
    }
}
