use std::fs;

const INPUT_FILEPATH: &str = "res/template/input.txt";

type Int = u32;

fn get_input_from_str(_string: &str) -> Int {
    0
}

fn get_input_from_file(filepath: &str) -> Int {
    get_input_from_str(&fs::read_to_string(filepath).expect("Could not open file"))
}

fn part1(_arg: &Int) -> Int {
    0
}

fn part2(_arg: &Int) -> Int {
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

    const EXAMPLE: &str = "";

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE)), 0);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 0);
    }
}
