use std::fs;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2018_day8_input.txt";

type Int = u32;
type InputContent = Vec<Int>;

fn get_input_from_str(string: &str) -> InputContent {
    let mut line_it = string.lines();
    line_it
        .next()
        .unwrap()
        .split(' ')
        .map(|nb| nb.parse::<Int>().unwrap())
        .collect()
}

fn get_input_from_file(filepath: &str) -> InputContent {
    get_input_from_str(&fs::read_to_string(filepath).expect("Could not open file"))
}

fn extract_metadata(nbs: &[Int]) -> (Int, &[Int]) {
    //dbg!("start", nbs.len());
    let nb_child = nbs[0];
    let nb_meta = nbs[1];
    let mut remaining = &nbs[2..];
    let mut ret = 0;
    for _ in 0..nb_child {
        let meta;
        (meta, remaining) = extract_metadata(remaining);
        ret += meta;
    }
    for _ in 0..nb_meta {
        ret += remaining[0];
        remaining = &remaining[1..];
    }
    //dbg!("end", ret, remaining.len());
    (ret, remaining)
}

fn part1(nbs: &InputContent) -> Int {
    let (nb, rem) = extract_metadata(nbs);
    assert!(rem.is_empty());
    nb
}

#[allow(clippy::trivially_copy_pass_by_ref, clippy::missing_const_for_fn)]
fn part2(_arg: &InputContent) -> Int {
    0
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_file(INPUT_FILEPATH);
    let res = part1(&data);
    println!("{:?}", res);
    assert_eq!(res, 40848);
    let res2 = part2(&data);
    println!("{:?}", res2);
    assert_eq!(res2, 0);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE: &str = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2";

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE)), 138);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 0);
    }
}
