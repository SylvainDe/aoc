use common::get_file_content;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2016_day3_input.txt";

type Int = u32;
type InputContent = Vec<Vec<Int>>;

fn parse_integer_list(str: &str) -> Vec<Int> {
    str.split(' ')
        .filter(|s| !s.is_empty())
        .map(|s| s.parse::<u32>().unwrap())
        .collect()
}

fn get_input_from_str(string: &str) -> InputContent {
    string.lines().map(parse_integer_list).collect()
}

fn get_input_from_file(filepath: &str) -> InputContent {
    get_input_from_str(&get_file_content(filepath))
}

fn is_triangle(nbs: &[Int]) -> bool {
    let mut sorted = nbs.to_owned();
    sorted.sort_unstable();
    if let [a, b, c] = &sorted[..] {
        if a + b > *c {
            return true;
        }
    }
    false
}

fn part1(arg: &InputContent) -> usize {
    arg.iter().filter(|nbs| is_triangle(nbs)).count()
}

#[allow(clippy::missing_const_for_fn)]
fn part2(_arg: &InputContent) -> Int {
    0
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_file(INPUT_FILEPATH);
    let res = part1(&data);
    println!("{:?}", res);
    assert_eq!(res, 993);
    let res2 = part2(&data);
    println!("{:?}", res2);
    assert_eq!(res2, 0);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE: &str = "5 10 25
   5    10     20
2 3 4";

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE)), 1);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 0);
    }
}
