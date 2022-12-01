use common::input::get_first_line_from_file;
use itertools::Itertools;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2016_day14_input.txt";

const SKIP_SLOW: bool = true;

fn get_hash(salt: &str, index: usize, stretched: bool) -> String {
    let nb = if stretched { 2017 } else { 1 };
    let mut s = format!("{}{}", salt, index);
    for _ in 0..nb {
        s = format!("{:?}", md5::compute(s));
    }
    s
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

fn produce_key(salt: &str, index_wanted: usize, stretched: bool) -> usize {
    let mut reps = Vec::new();
    let mut nb_found = 0;
    for i in 0..1000 {
        reps.push(find_repetitions(&get_hash(salt, i, stretched)));
    }
    for i in 0.. {
        // Compute and add new hash
        reps.push(find_repetitions(&get_hash(
            salt,
            (i + 1000) as usize,
            stretched,
        )));
        // Find first triplet
        if let Some((c, _)) = reps.get(i).unwrap().iter().find(|(_, cnt)| cnt >= &3) {
            for j in i + 1..=i + 1000 {
                // Find corresponding sequence of 5
                if reps
                    .get(j)
                    .unwrap()
                    .iter()
                    .any(|(c2, cnt2)| c == c2 && cnt2 >= &5)
                {
                    nb_found += 1;
                    if nb_found == index_wanted {
                        return i;
                    }
                    break;
                }
            }
        }
    }
    0
}

fn part1(salt: &str) -> usize {
    produce_key(salt, 64, false)
}

fn part2(salt: &str) -> usize {
    produce_key(salt, 64, true)
}

fn main() {
    let before = Instant::now();
    let data = get_first_line_from_file(INPUT_FILEPATH);
    //dbg!(&data);
    let res = part1(&data);
    println!("{:?}", res);
    assert_eq!(res, 18626);
    if !SKIP_SLOW {
        let res2 = part2(&data);
        println!("{:?}", res2);
        assert_eq!(res2, 20092);
    }
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    const SALT: &str = "abc";

    #[test]
    fn test_get_hash() {
        let stretched = false;
        assert_eq!(
            get_hash(SALT, 0, stretched),
            "577571be4de9dcce85a041ba0410f29f"
        );
        assert_eq!(
            get_hash(SALT, 18, stretched),
            "0034e0923cc38887a57bd7b1d4f953df"
        );
        assert_eq!(
            get_hash(SALT, 39, stretched),
            "347dac6ee8eeea4652c7476d0f97bee5"
        );
        assert_eq!(
            get_hash(SALT, 816, stretched),
            "3aeeeee1367614f3061d165a5fe3cac3"
        );
        assert_eq!(
            get_hash(SALT, 92, stretched),
            "ae2e85dd75d63e916a525df95e999ea0"
        );
        assert_eq!(
            get_hash(SALT, 200, stretched),
            "83501e9109999965af11270ef8d61a4f"
        );
        assert_eq!(
            get_hash(SALT, 22728, stretched),
            "26ccc731a8706e0c4f979aeb341871f0"
        );
        let stretched = true;
        assert_eq!(
            get_hash(SALT, 0, stretched),
            "a107ff634856bb300138cac6568c0f24"
        );
    }

    #[test]
    fn test_find_repetitions() {
        let stretched = false;
        assert_eq!(
            find_repetitions(&get_hash(SALT, 39, stretched)),
            vec![('e', 2,), ('e', 3,), ('e', 2,),]
        );
        assert_eq!(
            find_repetitions(&get_hash(SALT, 816, stretched)),
            vec![('e', 5,),]
        );
    }

    #[test]
    fn test_find_interesting_hash() {
        let stretched = false;
        assert_eq!(produce_key(SALT, 1, stretched), 39);
        assert_eq!(produce_key(SALT, 2, stretched), 92);
        assert_eq!(produce_key(SALT, 64, stretched), 22728);
        if !SKIP_SLOW {
            let stretched = true;
            assert_eq!(produce_key(SALT, 1, stretched), 10);
            assert_eq!(produce_key(SALT, 64, stretched), 22551);
        }
    }

    #[test]
    fn test_part1() {
        assert_eq!(part1(SALT), 22728);
    }

    #[test]
    fn test_part2() {
        if !SKIP_SLOW {
            assert_eq!(part2(SALT), 22551);
        }
    }
}
