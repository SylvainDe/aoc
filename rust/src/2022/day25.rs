// vi: set shiftwidth=4 tabstop=4 expandtab:
use common::input::check_answer;
use common::input::collect_lines;
use common::input::get_answers;
use common::input::get_file_content;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2022_day25_input.txt";
const ANSWERS_FILEPATH: &str = "../resources/year2022_day25_answer.txt";

type Int = i64;
type InputContent = Vec<String>;

fn get_input_from_str(string: &str) -> InputContent {
    collect_lines(string)
}

fn from_snafu(s: &str) -> Int {
    let mut n = 0;
    for c in s.chars() {
        n *= 5;
        n += match c {
            '2' => 2,
            '1' => 1,
            '0' => 0,
            '-' => -1,
            '=' => -2,
            _ => panic!("Unexpected value {c}"),
        }
    }
    n
}

fn to_snafu(n: Int) -> String {
    let mut n = n;
    let mut v = Vec::new();
    while n > 0 {
        n += 2; // Add 2 then remove 2
        let r = (n % 5) - 2;
        n /= 5;
        v.push(match r {
            2 => '2',
            1 => '1',
            0 => '0',
            -1 => '-',
            -2 => '=',
            _ => panic!("Unexpected value {r}"),
        });
    }
    v.reverse();
    v.iter().collect()
}

fn part1(arg: &InputContent) -> String {
    to_snafu(arg.iter().map(|s| from_snafu(s)).sum())
}

#[allow(clippy::missing_const_for_fn)]
fn main() {
    let before = Instant::now();
    let data = get_input_from_str(&get_file_content(INPUT_FILEPATH));
    let (ans, _) = get_answers(ANSWERS_FILEPATH);
    let solved = true;
    let res = part1(&data);
    check_answer(&res, ans, solved);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_conversion() {
        let values = Vec::from([
            (1, "1"),
            (2, "2"),
            (3, "1="),
            (4, "1-"),
            (5, "10"),
            (6, "11"),
            (7, "12"),
            (8, "2="),
            (9, "2-"),
            (10, "20"),
            (15, "1=0"),
            (20, "1-0"),
            (2022, "1=11-2"),
            (12345, "1-0---0"),
            (314159265, "1121-1110-1=0"),
        ]);
        for (n, s) in values {
            assert_eq!(n, from_snafu(s));
            assert_eq!(s, to_snafu(n));
        }
    }

    #[test]
    fn test_part1() {
        const EXAMPLE: &str = "1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122";

        assert_eq!(part1(&get_input_from_str(EXAMPLE)), "2=-1=0");
    }
}
