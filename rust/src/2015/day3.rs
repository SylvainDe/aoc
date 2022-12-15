// vi: set shiftwidth=4 tabstop=4 expandtab:
use common::input::get_first_line_from_file;
use std::collections::HashSet;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2015_day3_input.txt";

type Position = (i32, i32);

fn get_path(input: impl Iterator<Item = char>) -> HashSet<Position> {
    let mut x: i32 = 0;
    let mut y: i32 = 0;
    let mut pos = HashSet::new();
    pos.insert((x, y));
    for c in input {
        match c {
            '^' => x += 1,
            'v' => x -= 1,
            '<' => y -= 1,
            '>' => y += 1,
            _ => panic!("Unexpected value {}", c),
        }
        pos.insert((x, y));
    }
    pos
}

fn part1(input: &str) -> usize {
    get_path(input.chars()).len()
}

fn part2(input: &str) -> usize {
    let mut path1 = get_path(input.chars().step_by(2));
    let mut char_it = input.chars();
    char_it.next();
    path1.extend(get_path(char_it.step_by(2)));
    path1.len()
}

fn main() {
    let before = Instant::now();
    let data = get_first_line_from_file(INPUT_FILEPATH);
    let res = part1(&data);
    println!("{:?}", res);
    assert_eq!(res, 2081);
    let res2 = part2(&data);
    println!("{:?}", res2);
    assert_eq!(res2, 2341);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        assert_eq!(part1(""), 1);
        assert_eq!(part1(">"), 2);
        assert_eq!(part1("^>v<"), 4);
        assert_eq!(part1("^v^v^v^v^v"), 2);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(""), 1);
        assert_eq!(part2("^v"), 3);
        assert_eq!(part2("^>v<"), 3);
        assert_eq!(part2("^v^v^v^v^v"), 11);
    }
}
