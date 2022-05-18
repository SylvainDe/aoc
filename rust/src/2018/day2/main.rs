use std::borrow::ToOwned;
use std::collections::HashMap;
use std::fs;
use std::iter::zip;

const INPUT_FILEPATH: &str = "../resources/year2018_day2_input.txt";

type Int = u32;
type InputContent = Vec<String>;

fn get_input_from_str(string: &str) -> InputContent {
    string.lines().map(ToOwned::to_owned).collect()
}

fn get_input_from_file(filepath: &str) -> InputContent {
    get_input_from_str(&fs::read_to_string(filepath).expect("Could not open file"))
}

fn count(s: &str) -> HashMap<char, Int> {
    let mut counter = HashMap::<char, Int>::new();
    for c in s.chars() {
        let count = counter.entry(c).or_insert(0);
        *count += 1;
    }
    counter
}

fn part1(strings: &InputContent) -> Int {
    let mut nb2: Int = 0;
    let mut nb3: Int = 0;
    for s in strings {
        let count = count(s);
        nb2 += Int::from(count.values().any(|&val| val == 2));
        nb3 += Int::from(count.values().any(|&val| val == 3));
    }
    nb2 * nb3
}

fn part2(strings: &InputContent) -> String {
    for (i, si) in strings.iter().enumerate() {
        for (j, sj) in strings.iter().enumerate() {
            if i < j && si.len() == sj.len() {
                let same: String = zip(si.chars(), sj.chars())
                    .filter(|(c1, c2)| c1 == c2)
                    .map(|(c1, _)| c1)
                    .collect();
                if same.len() + 1 == si.len() {
                    return same;
                }
            }
        }
    }
    panic!("No result found");
}

fn main() {
    let data = get_input_from_file(INPUT_FILEPATH);
    let res = part1(&data);
    println!("{:?}", res);
    assert_eq!(res, 7657);
    let res2 = part2(&data);
    println!("{:?}", res2);
    assert_eq!(res2, "ivjhcadokeltwgsfsmqwrbnuy");
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE1: &str = "abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab";

    const EXAMPLE2: &str = "abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz";

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE1)), 12);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE2)), "fgij");
    }
}
