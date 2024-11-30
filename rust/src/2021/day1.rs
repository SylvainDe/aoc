// vi: set shiftwidth=4 tabstop=4 expandtab:
use common::input::check_answer;
use common::input::collect_from_lines;
use common::input::get_answers;
use common::input::get_file_content;
use itertools::Itertools as _;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2021_day1_input.txt";
const ANSWERS_FILEPATH: &str = "../resources/year2021_day1_answer.txt";

type Int = u32;
type InputContent = Vec<Int>;

fn get_input_from_str(string: &str) -> InputContent {
    collect_from_lines(string)
}

fn part1(depths: &InputContent) -> usize {
    depths.iter().tuple_windows().filter(|(a, b)| a < b).count()
}

fn part2(depths: &InputContent) -> usize {
    // Window(n + 1) > Window(n)
    // d(n+1) + d(n+2) + ... + d(n+1+windowsize) > d(n) + d(n+1) + ... + d(n+windowsize)
    // d(n+1+windowsize) > d(n)
    depths
        .iter()
        .tuple_windows()
        .filter(|(a, _, _, d)| a < d)
        .count()
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

    const EXAMPLE: &str = "199
200
208
210
200
207
240
269
260
263";

    #[test]
    fn input_from_str() {
        assert_eq!(
            get_input_from_str(EXAMPLE),
            vec![199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
        );
    }

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE)), 7);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 5);
    }
}
