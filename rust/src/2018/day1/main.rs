use std::collections::HashSet;
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
fn part2(arg: &InputContent) -> Int {
    let mut f: Int = 0;
    let mut frequencies = HashSet::<Int>::new();
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
    let data = get_input_from_file(INPUT_FILEPATH);
    let res = part1(&data);
    println!("{:?}", res);
    assert_eq!(res, 587);
    let res2 = part2(&data);
    println!("{:?}", res2);
    assert_eq!(res2, 83130);
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
