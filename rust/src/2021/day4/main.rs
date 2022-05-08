use std::fs::File;
use std::io::BufRead;
use std::io::BufReader;

const INPUT_FILEPATH: &str = "res/2021/day4/input.txt";

fn get_input_from_file(filepath: &str) -> u32 {
    let mut line_it = BufReader::new(File::open(filepath).expect("Could not open file")).lines();
    let first_line = line_it.next().unwrap().unwrap();
    let nbs: Vec<u32> = first_line
        .split(",")
        .map(|nb| nb.parse::<u32>().unwrap())
        .collect();
    println!("{:?}", nbs);
    for line in line_it {
        let s = line.unwrap();
        if !s.is_empty() {
            //let nbs: Vec<u32> = s.split(",").map(|nb| { nb.parse::<u32>().unwrap() }).collect();
            //println!("{:?}", nbs);
        }
    }
    0
}

fn part1(_arg: &u32) -> u32 {
    0
}

fn part2(_arg: &u32) -> u32 {
    0
}

fn main() {
    println!("Hello, world!");
    let commands = get_input_from_file(INPUT_FILEPATH);
    let res = part1(&commands);
    println!("{:?}", res);
    assert_eq!(res, 0);
    let res2 = part2(&commands);
    println!("{:?}", res2);
    assert_eq!(res2, 0);
}

#[cfg(test)]
mod tests {
    //use super::*;
}
