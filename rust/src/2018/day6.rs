use common::input::collect_from_lines_with_func;
use common::input::get_file_content;
use common::point_module;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2018_day6_input.txt";

type Int = i32;
type Point = point_module::Point<Int>;
type InputContent = Vec<Point>;

fn get_input_from_str(string: &str) -> InputContent {
    collect_from_lines_with_func(string, |s| Point::from_str_with_param(s, ", "))
}

#[allow(clippy::trivially_copy_pass_by_ref, clippy::missing_const_for_fn)]
fn part1(_arg: &InputContent) -> Int {
    // TODO: First step - filter interior points and exterior points
    0
}

#[allow(clippy::trivially_copy_pass_by_ref, clippy::missing_const_for_fn)]
fn part2(_arg: &InputContent) -> Int {
    0
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_str(&get_file_content(INPUT_FILEPATH));
    let res = part1(&data);
    println!("{:?}", res);
    assert_eq!(res, 0);
    let res2 = part2(&data);
    println!("{:?}", res2);
    assert_eq!(res2, 0);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE: &str = "1, 1
1, 6
8, 3
3, 4
5, 5
8, 9";

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE)), 0);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 0);
    }
}
