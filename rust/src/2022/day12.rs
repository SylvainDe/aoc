// vi: set shiftwidth=4 tabstop=4 expandtab:
use common::input::check_answer;
use common::input::get_answers;
use common::input::get_file_content;
use common::point_module;
use std::collections::HashMap;
use std::collections::VecDeque;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2022_day12_input.txt";
const ANSWERS_FILEPATH: &str = "../resources/year2022_day12_answer.txt";

type Int = u32;
type Point = point_module::Point<isize>;
type Grid = HashMap<Point, Int>;
type InputContent = (Grid, Point, Point);

#[allow(clippy::cast_possible_wrap)]
fn get_input_from_str(string: &str) -> InputContent {
    let mut start = None;
    let mut end = None;
    let mut grid = Grid::new();
    for (i, l) in string.lines().enumerate() {
        for (j, val) in l.chars().enumerate() {
            let pos = Point {
                x: i as isize,
                y: j as isize,
            };
            let mut c = val;
            if val == 'S' {
                start = Some(pos);
                c = 'a';
            } else if val == 'E' {
                end = Some(pos);
                c = 'z';
            }
            grid.insert(pos, c as Int - 'a' as Int);
        }
    }
    (grid, start.unwrap(), end.unwrap())
}

fn get_neighbours(Point { x, y }: &Point) -> Vec<Point> {
    [(-1, 0), (1, 0), (0, -1), (0, 1)]
        .iter()
        .map(|(dx, dy)| Point {
            x: x + dx,
            y: y + dy,
        })
        .collect()
}

fn get_accessible_neighbours(grid: &Grid, uphill: bool) -> HashMap<Point, HashMap<Point, Int>> {
    let mut access = HashMap::new();
    for (pos, &val) in grid {
        let d = access.entry(*pos).or_insert_with(HashMap::new);
        for pos2 in get_neighbours(pos) {
            if let Some(&val2) = grid.get(&pos2) {
                if if uphill {
                    val2 <= val + 1
                } else {
                    val <= val2 + 1
                } {
                    d.insert(pos2, 1);
                }
            }
        }
    }
    access
}

fn get_distances(grid: &Grid, start: Point, uphill: bool) -> HashMap<Point, Int> {
    let mut distances = HashMap::new();
    let mut deq = VecDeque::from([(0, start)]);
    let neigh = get_accessible_neighbours(grid, uphill);
    while let Some((d, pos)) = deq.pop_front() {
        if let Some(&old_d) = distances.get(&pos) {
            if old_d <= d {
                continue;
            }
        }
        distances.insert(pos, d);
        let neigh2 = &neigh[&pos];
        for (pos2, d2) in neigh2 {
            deq.push_back((d + d2, *pos2));
        }
    }
    distances
}

fn part1((grid, start, dest): &InputContent) -> Int {
    get_distances(grid, *start, true)[dest]
}

fn part2((grid, _start, dest): &InputContent) -> Int {
    *get_distances(grid, *dest, false)
        .iter()
        .filter(|(pos, _)| grid[pos] == 0)
        .map(|(_, d)| d)
        .min()
        .unwrap()
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_str(&get_file_content(INPUT_FILEPATH));
    let (ans, ans2) = get_answers(ANSWERS_FILEPATH);
    let solved = true;
    let res = part1(&data);
    check_answer(&res.to_string(), ans, solved);
    let res2 = part2(&data);
    check_answer(&res2.to_string(), ans2, solved);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE: &str = "Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi";

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE)), 31);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 29);
    }
}
