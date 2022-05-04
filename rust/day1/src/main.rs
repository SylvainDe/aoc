use std::fs::File;
use std::io::BufRead;
use std::io::BufReader;

const INPUT_FILEPATH: &str = "res/input.txt";

fn get_input(filepath: &str) -> Option<Vec<u32>> {
    let file = File::open(filepath).ok()?;
    let mut numbers: Vec<u32> = vec![];
    for line in BufReader::new(file).lines() {
        let n: u32 = line.ok()?.parse().ok()?;
        numbers.push(n)
    }
    Some(numbers)
}

fn main() {
    println!("Hello, world!");
    let numbers = get_input(INPUT_FILEPATH);
    println!("{:?}", numbers);
}

#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }
}
