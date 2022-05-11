use std::fs;

const INPUT_FILEPATH: &str = "res/2021/day6/input.txt";

type Int = usize;

fn get_input_from_str(string: &str) -> Vec<Int> {
    string
        .lines()
        .next()
        .unwrap()
        .split(',')
        .map(|s| s.parse::<Int>().unwrap())
        .collect()
}

fn get_input_from_file(filepath: &str) -> Vec<Int> {
    get_input_from_str(&fs::read_to_string(filepath).expect("Could not open file"))
}

fn get_generation_count(fishes: &Vec<Int>, nb_generation: Int) -> Int {
    let mut count = vec![0; 9];
    for f in fishes {
        count[*f] += 1;
    }
    for _ in 0..nb_generation {
        // Shift every generation
        let val = count.remove(0);
        // Add new generations
        count[6] += val;
        count.push(val);
    }
    count.iter().sum()
}

fn part1(fishes: &Vec<Int>) -> Int {
    get_generation_count(fishes, 80)
}

fn part2(fishes: &Vec<Int>) -> Int {
    get_generation_count(fishes, 256)
}

fn main() {
    let fishes = get_input_from_file(INPUT_FILEPATH);
    let res = part1(&fishes);
    println!("{:?}", res);
    assert_eq!(res, 390011);
    let res2 = part2(&fishes);
    println!("{:?}", res2);
    assert_eq!(res2, 1746710169834);
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE: &str = "3,4,3,1,2";

    #[test]
    fn test_generation_count() {
        let input = get_input_from_str(EXAMPLE);
        assert_eq!(get_generation_count(&input, 0), 5);
        assert_eq!(get_generation_count(&input, 1), 5);
        assert_eq!(get_generation_count(&input, 2), 6);
        assert_eq!(get_generation_count(&input, 3), 7);
        assert_eq!(get_generation_count(&input, 4), 9);
        assert_eq!(get_generation_count(&input, 5), 10);
        assert_eq!(get_generation_count(&input, 6), 10);
        assert_eq!(get_generation_count(&input, 7), 10);
        assert_eq!(get_generation_count(&input, 8), 10);
        assert_eq!(get_generation_count(&input, 8), 10);
        assert_eq!(get_generation_count(&input, 18), 26);
        assert_eq!(get_generation_count(&input, 80), 5934);
        assert_eq!(get_generation_count(&input, 256), 26984457539);
    }

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE)), 5934);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 26984457539);
    }
}
