// vi: set shiftwidth=4 tabstop=4 expandtab:
use common::input::check_answer;
use common::input::collect_from_lines;
use common::input::get_answers;
use common::input::get_file_content;
use std::collections::HashSet;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2018_day1_input.txt";
const ANSWERS_FILEPATH: &str = "../resources/year2018_day1_answer.txt";

type Int = i32;
type InputContent = Vec<Int>;

fn get_input_from_str(string: &str) -> InputContent {
    collect_from_lines(string)
}

fn part1(arg: &InputContent) -> Int {
    arg.iter().sum()
}

fn part2(arg: &InputContent) -> Int {
    let mut f: Int = 0;
    let mut frequencies = HashSet::new();
    loop {
        for d in arg {
            f += d;
            if frequencies.contains(&f) {
                return f;
            }
            frequencies.insert(f);
        }
    }
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

    const EXAMPLE: &str = "+1
-2
+3
+1";

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE)), 3);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 2);
    }
}
