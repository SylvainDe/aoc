// vi: set shiftwidth=4 tabstop=4 expandtab:
use common::input::check_answer;
use common::input::get_answers;
use common::input::get_first_line_from_file;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2015_day4_input.txt";
const ANSWERS_FILEPATH: &str = "../resources/year2015_day4_answer.txt";

type Int = u32;
const SKIP_SLOW: bool = true;

fn digest_starts_with(data: &str, prefix: &str) -> bool {
    let digest = format!("{:?}", md5::compute(data));
    digest.starts_with(prefix)
}

fn find_coin(data: &str, prefix: &str) -> Int {
    for i in 0.. {
        let s = format!("{data}{i}");
        if digest_starts_with(&s, prefix) {
            return i;
        }
    }
    panic!("No value found");
}

fn part1(input: &str) -> Int {
    find_coin(input, "00000")
}

fn part2(input: &str) -> Int {
    find_coin(input, "000000")
}

fn main() {
    let before = Instant::now();
    let data = get_first_line_from_file(INPUT_FILEPATH);
    let (ans, ans2) = get_answers(ANSWERS_FILEPATH);
    let solved = true;
    let res = part1(&data);
    check_answer(&res.to_string(), ans, solved);
    if !SKIP_SLOW {
        let res2 = part2(&data);
        check_answer(&res2.to_string(), ans2, solved);
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
