// vi: set shiftwidth=4 tabstop=4 expandtab:
use common::input::check_answer;
use common::input::collect_from_lines;
use common::input::get_answers;
use common::input::get_file_content;
use core::str::FromStr;
use regex::Regex;
use std::collections::BinaryHeap;
use std::collections::HashMap;
use std::collections::HashSet;
use std::sync::LazyLock;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2018_day7_input.txt";
const ANSWERS_FILEPATH: &str = "../resources/year2018_day7_answer.txt";

#[derive(Debug, PartialEq)]
struct Dependency {
    first: char,
    last: char,
}

impl FromStr for Dependency {
    type Err = ();
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        // Step C must be finished before step A can begin.
        static RE: LazyLock<Regex> = LazyLock::new(|| {
            Regex::new(concat!(
                r"^Step (?P<first>.) must be finished before step (?P<last>.) can begin\.$"
            ))
            .unwrap()
        });
        let c = RE.captures(s).ok_or(())?;
        let first_char = |s: &str| c.name(s).ok_or(())?.as_str().chars().next().ok_or(());
        Ok(Self {
            first: first_char("first")?,
            last: first_char("last")?,
        })
    }
}

type InputContent = Vec<Dependency>;

fn get_input_from_str(string: &str) -> InputContent {
    collect_from_lines(string)
}

fn build_dependencies(deps: &InputContent) -> HashMap<char, Vec<char>> {
    let mut needs = HashMap::new();
    for Dependency { first, last } in deps {
        needs.entry(*first).or_insert_with(Vec::new);
        needs.entry(*last).or_insert_with(Vec::new).push(*first);
    }
    needs
}

fn part1(deps: &InputContent) -> String {
    let needs = build_dependencies(deps);
    let mut done = Vec::new();
    loop {
        let mut candidates = Vec::new();
        for (step, lst) in &needs {
            if !done.contains(step) && lst.iter().filter(|s| !done.contains(s)).count() == 0 {
                candidates.push(*step);
            }
        }
        candidates.sort_unstable();
        match candidates.first() {
            None => break,
            Some(c) => done.push(*c),
        }
    }
    done.into_iter().collect()
}

type Timestamp = i32;
fn part2(deps: &InputContent, duration_step_a: i32, nb_workers: usize) -> Timestamp {
    let needs = build_dependencies(deps);
    let nb_step = needs.len();
    let mut time = 0;
    let mut workers = BinaryHeap::<(Timestamp, char)>::new();
    let mut in_progress = HashSet::new();
    let mut done = HashSet::new();
    loop {
        // Switch to next finished worker(s) and take into account finished task(s)
        //  - remove worker
        //  - add task to done
        if let Some((timestamp, _step)) = workers.peek() {
            let timestamp = -timestamp;
            assert!(timestamp >= time, "Task should be already finished");
            time = timestamp;
            while let Some((timestamp2, step2)) = workers.pop() {
                if -timestamp2 == timestamp {
                    done.insert(step2);
                } else {
                    workers.push((timestamp2, step2));
                    break;
                }
            }
        }
        // Stop if all tasks are done
        if done.len() == nb_step {
            return time;
        }
        // Compute new candidates
        let mut candidates = Vec::new();
        for (step, lst) in &needs {
            if !in_progress.contains(step)
                && !done.contains(step)
                && lst.iter().filter(|s| !done.contains(s)).count() == 0
            {
                candidates.push(*step);
            }
        }
        candidates.sort_unstable();
        // Assign tasks to be done to available workers
        assert!(workers.len() < nb_workers);
        for step in candidates {
            if workers.len() < nb_workers {
                let duration = step as i32 - 'A' as i32 + duration_step_a;
                let timestamp = duration + time;
                workers.push((-timestamp, step));
                in_progress.insert(step);
            }
        }
    }
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_str(&get_file_content(INPUT_FILEPATH));
    let (ans, ans2) = get_answers(ANSWERS_FILEPATH);
    let solved = true;
    let res = part1(&data);
    check_answer(&res, ans, solved);
    let res2 = part2(&data, 61, 5);
    check_answer(&res2.to_string(), ans2, solved);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE: &str = "Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.";
    #[test]
    fn test_dep_from_str() {
        assert!(Dependency::from_str("").is_err());
        assert_eq!(
            Dependency::from_str("Step C must be finished before step A can begin."),
            Ok(Dependency {
                first: 'C',
                last: 'A',
            })
        );
    }

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE)), "CABDFE");
    }
    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE), 1, 2), 15);
    }
}
