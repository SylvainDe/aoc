// vi: set shiftwidth=4 tabstop=4 expandtab:
use common::input::get_first_line_from_file;
use std::collections::HashSet;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2022_day6_input.txt";

fn get_different_char(s: &str, winsize: usize) -> usize {
    for (i, w) in s
        .chars()
        .collect::<Vec<char>>()
        .windows(winsize)
        .enumerate()
    {
        let s = w.iter().copied().collect::<HashSet<char>>();
        if s.len() == winsize {
            return i + winsize;
        }
    }
    panic!("Unexpected");
}

fn part1(s: &str) -> usize {
    get_different_char(s, 4)
}

fn part2(s: &str) -> usize {
    get_different_char(s, 14)
}

fn main() {
    let before = Instant::now();
    let data = get_first_line_from_file(INPUT_FILEPATH);
    let res = part1(&data);
    println!("{:?}", res);
    assert_eq!(res, 1850);
    let res2 = part2(&data);
    println!("{:?}", res2);
    assert_eq!(res2, 2823);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        assert_eq!(part1("mjqjpqmgbljsphdztnvjfqwrcgsmlb"), 7);
        assert_eq!(part1("bvwbjplbgvbhsrlpgdmjqwftvncz"), 5);
        assert_eq!(part1("nppdvjthqldpwncqszvftbrmjlhg"), 6);
        assert_eq!(part1("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"), 10);
        assert_eq!(part1("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"), 11);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2("mjqjpqmgbljsphdztnvjfqwrcgsmlb"), 19);
        assert_eq!(part2("bvwbjplbgvbhsrlpgdmjqwftvncz"), 23);
        assert_eq!(part2("nppdvjthqldpwncqszvftbrmjlhg"), 23);
        assert_eq!(part2("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"), 29);
        assert_eq!(part2("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"), 26);
    }
}
