use common::collect_lines;
use common::get_file_content;
use std::cmp::Reverse;
use std::collections::BinaryHeap;
use std::collections::HashMap;
use std::collections::VecDeque;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2016_day24_input.txt";

type Int = usize;
type Point = (Int, Int);
type Graph = HashMap<Point, char>;

fn build_graph(string: &str) -> HashMap<Point, char> {
    let mut g = HashMap::<Point, char>::new();
    for (i, line) in collect_lines(string).iter().enumerate() {
        for (j, c) in line.chars().enumerate() {
            match c {
                '#' => (),
                _ => {
                    g.insert((i, j), c);
                }
            }
        }
    }
    g
}

fn get_input_from_str(string: &str) -> Graph {
    build_graph(string)
}

fn get_input_from_file(filepath: &str) -> Graph {
    get_input_from_str(&get_file_content(filepath))
}

fn neighbours(p: &Point) -> Vec<Point> {
    let (x, y) = p;
    vec![(x + 1, *y), (x - 1, *y), (*x, y + 1), (*x, y - 1)]
}

fn part1(g: &Graph) -> Int {
    // Compute interesting points
    let interesting_points = g
        .iter()
        .filter(|(_, c)| **c != '.')
        .map(|(p, c)| (*p, *c))
        .collect::<Vec<(Point, char)>>();
    // Compute starting point
    let start = interesting_points
        .iter()
        .filter(|(_, c)| *c == '0')
        .map(|(p, _)| *p)
        .next()
        .unwrap();
    // Compute interesting distances
    let mut interesting_dist = HashMap::new(); // Should we use hashmap of hashmap instead ?
    for (p, _) in &interesting_points {
        let mut dist = HashMap::new();
        let mut deq = VecDeque::from([(*p, 0)]);
        while let Some((p2, d)) = deq.pop_front() {
            if let std::collections::hash_map::Entry::Vacant(e) = dist.entry(p2) {
                e.insert(d);
                for n in neighbours(&p2) {
                    if g.contains_key(&n) && !dist.contains_key(&n) {
                        deq.push_back((n, d + 1));
                    }
                }
            }
        }
        for (p2, _) in &interesting_points {
            interesting_dist.insert((p, p2), dist[p2]);
        }
    }
    // Check interesting distances
    for ((p1, p2), d) in &interesting_dist {
        assert!(interesting_dist.get(&(p2, p1)) == Some(d));
    }
    // Compute best path
    let mut distances = BinaryHeap::new();
    distances.push(Reverse((0, vec![start])));
    while let Some(Reverse((d, points))) = distances.pop() {
        let last = points.last().unwrap();
        let mut added = false;
        for ((p1, p2), d2) in &interesting_dist {
            if &last == p1 && !points.contains(p2) {
                let mut points2 = points.clone();
                points2.push(**p2);
                distances.push(Reverse(((d + d2), points2)));
                added = true;
            }
        }
        if !added {
            return d;
        }
    }
    0
}

#[allow(clippy::missing_const_for_fn)]
fn part2(_arg: &Graph) -> Int {
    0
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_file(INPUT_FILEPATH);
    let res = part1(&data);
    println!("{:?}", res);
    assert_eq!(res, 462);
    let res2 = part2(&data);
    println!("{:?}", res2);
    assert_eq!(res2, 0);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE: &str = "###########
#0.1.....2#
#.#######.#
#4.......3#
###########";

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE)), 14);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 0);
    }
}
