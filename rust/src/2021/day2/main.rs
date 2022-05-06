use std::fs::File;
use std::io::BufReader;

const INPUT_FILEPATH: &str = "res/2021/day2/input.txt";

fn get_input(filepath: &str) -> () {
    BufReader::new(File::open(filepath).expect("Could not open file"));
}

fn main() {
    println!("Hello, world!");
    get_input(INPUT_FILEPATH);
}

#[cfg(test)]
mod tests {
    #[test]
    fn part1_todo() {
        assert_eq!(2 + 2, 4);
    }
}
