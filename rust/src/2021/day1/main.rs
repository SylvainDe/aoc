use itertools::Itertools;
use std::fs::File;
use std::io::BufRead;
use std::io::BufReader;

const INPUT_FILEPATH: &str = "res/2021/day1/input.txt";

type Int = u32;

fn get_input(filepath: &str) -> Vec<Int> {
    BufReader::new(File::open(filepath).expect("Could not open file"))
        .lines()
        .map(|line| {
            line.unwrap()
                .parse::<Int>()
                .expect("Could not convert line to integer")
        })
        .collect()
}

fn part1(depths: &[Int]) -> usize {
    depths.iter().tuple_windows().filter(|(a, b)| a < b).count()
}

fn part2(depths: &[Int]) -> usize {
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
    println!("Hello, world!");
    let numbers = get_input(INPUT_FILEPATH);
    println!("{:?}", part1(&numbers));
    println!("{:?}", part2(&numbers));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn part1_provided_test() {
        let numbers: Vec<Int> = vec![99, 200, 208, 210, 200, 207, 240, 269, 260, 263];
        assert_eq!(part1(&numbers), 7);
    }

    #[test]
    fn part2_provided_test() {
        let numbers: Vec<Int> = vec![99, 200, 208, 210, 200, 207, 240, 269, 260, 263];
        assert_eq!(part2(&numbers), 5);
    }
}
