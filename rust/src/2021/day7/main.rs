use std::cmp::min;
use std::fs;

const INPUT_FILEPATH: &str = "../resources/year2021_day7_input.txt";

type Int = i32;
type InputContent = Vec<Int>;

fn get_input_from_str(string: &str) -> InputContent {
    string
        .lines()
        .next()
        .unwrap()
        .split(',')
        .map(|s| s.parse::<Int>().expect("Could not convert line to integer"))
        .collect()
}

fn get_input_from_file(filepath: &str) -> InputContent {
    get_input_from_str(&fs::read_to_string(filepath).expect("Could not open file"))
}

fn get_fuel_cost_for_position(positions: &[Int], target: Int) -> Int {
    positions.iter().map(|n| (n - target).abs()).sum()
}

fn get_fuel_cost_for_position2(positions: &[Int], target: Int) -> Int {
    positions
        .iter()
        .map(|n| {
            let d = (n - target).abs();
            d * (d + 1) / 2
        })
        .sum()
}

fn part1(positions: &InputContent) -> Int {
    let mut positions = positions.clone();
    positions.sort_unstable();
    // Get cost around median positions
    // There is a single median position: there are the same
    // numbers of crabs on each side: if we go left or right,
    // the number of crabs getting further is bigger than the
    // number of crabs getting closer
    let n = positions.len();
    min(
        get_fuel_cost_for_position(&positions, positions[n / 2]),
        get_fuel_cost_for_position(&positions, positions[(n + 1) / 2]),
    )
}

#[allow(
    clippy::cast_possible_wrap,
    clippy::cast_possible_truncation,
    clippy::cast_precision_loss
)]
fn part2(positions: &InputContent) -> Int {
    // 1. Computing the minimal cost with a square cost: C = d²
    //    can be done:
    //       F(x) = (p1 - x)² + (p2 - x)² + ... + (pn - x)²
    //       F(x) = nx² - 2x(p1 + p2 + ... + pn) + (p1² + p2² + ... + pn²)
    //       F²(x) = 2nx - 2(p1 + p2 + ... + pn)
    //       F'(x) = 0 <=> x = (p1 + ... + pn) / n
    //
    // 2. Moving d cost C = (d+1)*d/2 which is slightly trickier to
    //    optimise as it involves computing absolute values.
    // 3. Using the best solution for problem 1 works for problem 2 but I don't know why
    // Computing the minimal cost with a square cost: C = d² can be done:
    //  F(x) = (p1 - x)² + (p2 - x)² + ... + (pn - x)²
    //  F(x) = nx² - 2x(p1 + p2 + ... + pn) + (p1² + p2² + ... + pn²)
    //  F²(x) = 2nx - 2(p1 + p2 + ... + pn)
    //  F'(x) = 0 <=> x = (p1 + ... + pn) / n
    let avg = (positions.iter().sum::<Int>() / positions.len() as Int) as f32;
    let f = avg.floor() as Int;
    min(
        get_fuel_cost_for_position2(positions, f),
        get_fuel_cost_for_position2(positions, f + 1),
    )
}

fn main() {
    let positions = get_input_from_file(INPUT_FILEPATH);
    let res = part1(&positions);
    println!("{:?}", res);
    assert_eq!(res, 343_468);
    let res2 = part2(&positions);
    println!("{:?}", res2);
    assert_eq!(res2, 96_086_265);
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE: &str = "16,1,2,0,4,2,7,1,2,14";

    #[test]
    fn input_from_str() {
        assert_eq!(
            get_input_from_str(EXAMPLE),
            vec![16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
        );
    }

    #[test]
    fn test_get_fuel_cost_for_position() {
        let positions = get_input_from_str(EXAMPLE);
        assert_eq!(get_fuel_cost_for_position(&positions, 1), 41);
        assert_eq!(get_fuel_cost_for_position(&positions, 2), 37);
        assert_eq!(get_fuel_cost_for_position(&positions, 3), 39);
        assert_eq!(get_fuel_cost_for_position(&positions, 10), 71);
    }

    #[test]
    fn test_get_fuel_cost_for_position2() {
        let positions = get_input_from_str(EXAMPLE);
        assert_eq!(get_fuel_cost_for_position2(&positions, 2), 206);
        assert_eq!(get_fuel_cost_for_position2(&positions, 5), 168);
    }

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE)), 37);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 168);
    }
}
