use std::fs;

const INPUT_FILEPATH: &str = "../resources/year2018_day1_input.txt";

type Int = i32;
type InputContent = Vec<Int>;

#[allow(clippy::missing_const_for_fn)]
fn get_input_from_str(string: &str) -> InputContent {
    string.lines().map(|l| l.parse::<Int>().unwrap()).collect()
}

fn get_input_from_file(filepath: &str) -> InputContent {
    get_input_from_str(&fs::read_to_string(filepath).expect("Could not open file"))
}

#[allow(clippy::trivially_copy_pass_by_ref, clippy::missing_const_for_fn)]
fn part1(arg: &InputContent) -> Int {
    arg.iter().sum()
}

#[allow(clippy::trivially_copy_pass_by_ref, clippy::missing_const_for_fn)]
fn part2(_arg: &InputContent) -> Int {
    0
}

fn main() {
    let data = get_input_from_file(INPUT_FILEPATH);
    let res = part1(&data);
    println!("{:?}", res);
    assert_eq!(res, 0);
    let res2 = part2(&data);
    println!("{:?}", res2);
    assert_eq!(res2, 0);
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
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 0);
    }
}
