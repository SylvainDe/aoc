// vi: set shiftwidth=4 tabstop=4 expandtab:
use common::input::check_answer;
use common::input::get_answers;
use common::input::get_first_line_from_file;
use regex::Regex;
use std::sync::LazyLock;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2018_day9_input.txt";
const ANSWERS_FILEPATH: &str = "../resources/year2018_day9_answer.txt";

type Int = u32;
type InputContent = Int;

fn get_input_from_str(string: &str) -> InputContent {
    static RE: LazyLock<Regex> = LazyLock::new(|| {
        Regex::new(concat!(
            r"^(?P<nb_players>\d+) players; last marble is worth (\d+) points$"
        ))
        .unwrap()
    });
    let c = RE.captures(string).ok_or(()).unwrap();
    let get_field = |s: &str| c.name(s).ok_or(());
    let to_int = |s: &str| get_field(s)?.as_str().parse::<Int>().map_err(|_| {});
    to_int("nb_players").unwrap()
}

#[expect(
    clippy::trivially_copy_pass_by_ref,
    clippy::missing_const_for_fn,
    reason = "Not implemented yet"
)]
fn part1(_arg: &InputContent) -> Int {
    0
}

#[expect(
    clippy::trivially_copy_pass_by_ref,
    clippy::missing_const_for_fn,
    reason = "Not implemented yet"
)]
fn part2(_arg: &InputContent) -> Int {
    0
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_str(&get_first_line_from_file(INPUT_FILEPATH));
    let (ans, ans2) = get_answers(ANSWERS_FILEPATH);
    let solved = false;
    let res = part1(&data);
    check_answer(&res.to_string(), ans, solved);
    let res2 = part2(&data);
    check_answer(&res2.to_string(), ans2, solved);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE: &str = "424 players; last marble is worth 71482 points";

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE)), 0);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 0);
    }
}
