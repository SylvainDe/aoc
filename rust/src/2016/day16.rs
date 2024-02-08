// vi: set shiftwidth=4 tabstop=4 expandtab:
use common::input::check_answer;
use common::input::get_answers;
use common::input::get_first_line_from_file;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2016_day16_input.txt";
const ANSWERS_FILEPATH: &str = "../resources/year2016_day16_answer.txt";

const SKIP_SLOW: bool = true;
type InputContent = String;

fn generate_data(initial_state: &str, len: usize) -> String {
    let mut res = initial_state.chars().collect::<Vec<char>>();
    while res.len() < len {
        let b = res
            .iter()
            .rev()
            .map(|c| match c {
                '0' => '1',
                '1' => '0',
                _ => *c,
            })
            .collect::<Vec<char>>();
        res.push('0');
        res.extend(b);
    }
    res.iter().collect::<String>()
}

fn checksum(data: &str) -> String {
    assert!(data.len() % 2 == 0);
    let mut v = data.chars().collect::<Vec<char>>();
    while v.len() % 2 == 0 {
        v = v
            .chunks(2)
            .map(|s| {
                assert!(s.len() == 2);
                if s[0] == s[1] {
                    '1'
                } else {
                    '0'
                }
            })
            .collect();
    }
    v.iter().collect::<String>()
}

fn disk_checksum(initial_state: &str, len: usize) -> String {
    let d = &generate_data(initial_state, len)[..len];
    checksum(d)
}

fn part1(arg: &InputContent) -> String {
    disk_checksum(arg, 272)
}

fn part2(arg: &InputContent) -> String {
    disk_checksum(arg, 35_651_584)
}

fn main() {
    let before = Instant::now();
    let data = get_first_line_from_file(INPUT_FILEPATH);
    let (ans, ans2) = get_answers(ANSWERS_FILEPATH);
    let solved = true;
    let res = part1(&data);
    check_answer(&res, ans, solved);
    if !SKIP_SLOW {
        let res2 = part2(&data);
        check_answer(&res2, ans2, solved);
    }
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_generate_data() {
        assert_eq!(generate_data("1", 3), "100");
        assert_eq!(generate_data("0", 3), "001");
        assert_eq!(generate_data("11111", 11), "11111000000");
        assert_eq!(
            generate_data("111100001010", 20),
            "1111000010100101011110000"
        );
        assert_eq!(generate_data("10000", 20), "10000011110010000111110");
    }

    #[test]
    fn test_checksum() {
        assert_eq!(checksum("110010110100"), "100");
    }

    #[test]
    fn test_disk_checksum() {
        assert_eq!(disk_checksum("10000", 20), "01100");
    }
}
