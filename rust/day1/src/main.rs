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

fn main() {
    println!("Hello, world!");
    let numbers = get_input(INPUT_FILEPATH);
    let s: Int = numbers.iter().sum();
    println!("{:?}", s);
}

#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }
}
