use common::get_first_line_from_file;
use itertools::Itertools;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2016_day14_input.txt";

type Int = u32;
const SKIP_SLOW: bool = true;

fn get_input_from_file(filepath: &str) -> String {
    get_first_line_from_file(filepath)
}

fn get_hash(salt: &str, index: Int, stretched: bool) -> String {
    let nb = if stretched { 2017 } else { 1 };
    let mut s = format!("{}{}", salt, index);
    for _ in 0..nb {
        s = format!("{:?}", md5::compute(s));
    }
    s
}

fn find_triplet(s: &str) -> Option<char> {
    s.chars()
        .tuple_windows()
        .filter(|(a, b, c)| a == b && b == c)
        .map(|(a, _, _)| a)
        .next()
}

fn find_5_repetitions(s: &str, repeated: char) -> bool {
    s.chars()
        .tuple_windows()
        .any(|(a, b, c, d, e)| repeated == a && a == b && b == c && c == d && d == e)
}

fn find_repetitions(s: &str) -> Vec<(char, usize)> {
    s.chars()
        .map(|c| (c, 1))
        .coalesce(|(c, n), (d, m)| {
            if c == d {
                Ok((c, n + m))
            } else {
                Err(((c, n), (d, m)))
            }
        })
        .filter(|(_, cnt)| *cnt > 1)
        .collect()
}

fn produce_key(salt: &str, index_wanted: Int, stretched: bool) -> Int {
    let mut nb_found = 0;
    // Naive implementation - everything is computed so many times :(
    // A better implementation would compute find_repetitions(&get_hash(salt, i, stretched))
    // only per index
    for i in 0.. {
        if let Some(c) = find_triplet(&get_hash(salt, i, stretched)) {
            let mut found = false;
            for j in i + 1..=i + 1000 {
                if find_5_repetitions(&get_hash(salt, j, stretched), c) {
                    found = true;
                    break;
                }
            }
            if found {
                nb_found += 1;
                if nb_found == index_wanted {
                    return i;
                }
            }
        }
    }
    0
}

fn part1(salt: &str) -> Int {
    produce_key(salt, 64, false)
}

#[allow(clippy::missing_const_for_fn)]
fn part2(_arg: &str) -> Int {
    0
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_file(INPUT_FILEPATH);
    if !SKIP_SLOW {
        let res = part1(&data);
        println!("{:?}", res);
        assert_eq!(res, 18626);
    }
    let res2 = part2(&data);
    println!("{:?}", res2);
    assert_eq!(res2, 0);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE: &str = "";

    #[test]
    fn test_get_hash() {
        let salt = "abc";
        let stretched = false;
        assert_eq!(
            get_hash(salt, 0, stretched),
            "577571be4de9dcce85a041ba0410f29f"
        );
        assert_eq!(
            get_hash(salt, 18, stretched),
            "0034e0923cc38887a57bd7b1d4f953df"
        );
        assert_eq!(
            get_hash(salt, 39, stretched),
            "347dac6ee8eeea4652c7476d0f97bee5"
        );
        assert_eq!(
            get_hash(salt, 816, stretched),
            "3aeeeee1367614f3061d165a5fe3cac3"
        );
        assert_eq!(
            get_hash(salt, 92, stretched),
            "ae2e85dd75d63e916a525df95e999ea0"
        );
        assert_eq!(
            get_hash(salt, 200, stretched),
            "83501e9109999965af11270ef8d61a4f"
        );
        assert_eq!(
            get_hash(salt, 22728, stretched),
            "26ccc731a8706e0c4f979aeb341871f0"
        );
        let stretched = true;
        assert_eq!(
            get_hash(salt, 0, stretched),
            "a107ff634856bb300138cac6568c0f24"
        );
    }

    #[test]
    fn test_find_interesting_hash() {
        let salt = "abc";
        let stretched = false;
        assert_eq!(find_triplet(&get_hash(salt, 38, stretched)), None);
        assert_eq!(find_triplet(&get_hash(salt, 39, stretched)), Some('e'));
        assert_eq!(
            find_5_repetitions(&get_hash(salt, 40, stretched), 'e'),
            stretched
        );
        assert_eq!(
            find_5_repetitions(&get_hash(salt, 816, stretched), 'e'),
            true
        );
        assert_eq!(produce_key(salt, 1, stretched), 39);
        assert_eq!(produce_key(salt, 2, stretched), 92);
        if !SKIP_SLOW {
            assert_eq!(produce_key(salt, 64, stretched), 22728);
        }
        assert_eq!(
            find_repetitions(&get_hash(salt, 39, stretched)),
            vec![('e', 2,), ('e', 3,), ('e', 2,),]
        );
        assert_eq!(
            find_repetitions(&get_hash(salt, 816, stretched)),
            vec![('e', 5,),]
        );
    }

    #[test]
    fn test_part1() {
        if !SKIP_SLOW {
            let salt = "abc";
            assert_eq!(part1(salt), 22728);
        }
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), 0);
    }
}
