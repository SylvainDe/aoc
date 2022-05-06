use itertools::Itertools;
use std::fs::File;
use std::io::BufRead;
use std::io::BufReader;

const INPUT_FILEPATH: &str = "res/input.txt";

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

fn part1(depths: Vec<Int>) -> usize {
    depths.iter().tuple_windows().filter(|(a, b)| a < b).count()
}

fn main() {
    println!("Hello, world!");
    let numbers = get_input(INPUT_FILEPATH);
    println!("{:?}", part1(numbers));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }

    #[test]
    fn part1_provided_test() {
        let numbers: Vec<Int> = vec![99, 200, 208, 210, 200, 207, 240, 269, 260, 263];
        assert_eq!(part1(numbers), 7);
    }
}
