// vi: set shiftwidth=4 tabstop=4 expandtab:
use common::input::check_answer;
use common::input::collect_from_lines;
use common::input::get_answers;
use common::input::get_file_content;
use core::str::FromStr;
use regex::Regex;
use std::collections::HashMap;
use std::sync::LazyLock;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2018_day4_input.txt";
const ANSWERS_FILEPATH: &str = "../resources/year2018_day4_answer.txt";

type Int = u32;

#[derive(Debug, Eq, Ord, PartialEq, PartialOrd)]
enum Action {
    ShiftBegins(Int),
    FallsAsleep,
    WakesUp,
}

impl FromStr for Action {
    type Err = ();
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "falls asleep" => Ok(Self::FallsAsleep),
            "wakes up" => Ok(Self::WakesUp),
            _ => {
                let (_, s) = s.split_once('#').ok_or(())?;
                let (id, _) = s.split_once(' ').ok_or(())?;
                Ok(Self::ShiftBegins(id.parse().map_err(|_| {})?))
            }
        }
    }
}

#[derive(Debug, Eq, Ord, PartialEq, PartialOrd, Hash, Clone, Copy)]
struct Timestamp {
    year: Int,
    month: Int,
    day: Int,
    hour: Int,
    minute: Int,
}

impl FromStr for Timestamp {
    type Err = ();
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        // [1518-11-01 00:00
        static RE: LazyLock<Regex> = LazyLock::new(|| {
            Regex::new(
                "^\\[(?P<year>\\d+)-(?P<month>\\d+)-(?P<day>\\d+) (?P<hour>\\d+):(?P<minute>\\d+)",
            )
            .unwrap()
        });
        let c = RE.captures(s).ok_or(())?;
        let to_int = |s: &str| c.name(s).ok_or(())?.as_str().parse::<Int>().map_err(|_| {});
        Ok(Self {
            year: to_int("year")?,
            month: to_int("month")?,
            day: to_int("day")?,
            hour: to_int("hour")?,
            minute: to_int("minute")?,
        })
    }
}

#[derive(Debug, Eq, Ord, PartialEq, PartialOrd)]
struct Event {
    timestamp: Timestamp,
    action: Action,
}

impl FromStr for Event {
    type Err = ();
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let (ts, action) = s.split_once("] ").ok_or(())?;
        Ok(Self {
            timestamp: ts.parse().map_err(|()| {})?,
            action: action.parse().map_err(|()| {})?,
        })
    }
}
type InputContent = Vec<Event>;

fn get_input_from_str(string: &str) -> InputContent {
    let mut entries = collect_from_lines(string);
    entries.sort();
    entries
}

fn find_sleeping_guard(events: &InputContent, is_part1: bool) -> Int {
    let mut guard = None;
    let mut sleep_start = None;
    let mut sleeps_total = HashMap::new();
    let mut sleeps_per_guard_per_min = HashMap::new();
    let mut sleeps_per_guard_and_min = HashMap::new();
    for e in events {
        match e.action {
            Action::ShiftBegins(id) => guard = Some(id),
            Action::FallsAsleep => sleep_start = Some(e.timestamp),
            Action::WakesUp => {
                let guard = guard.unwrap();
                let start = sleep_start.unwrap();
                let end = e.timestamp;
                // Assume many things about time values
                let nb_year = end.year - start.year;
                let nb_month = 12 * nb_year + end.month - start.month;
                let nb_day = 30 * nb_month + end.day - start.day;
                let nb_hour = 24 * nb_day + end.hour - start.hour;
                let nb_min = 60 * nb_hour + end.minute - start.minute;
                let total_count = sleeps_total.entry(guard).or_insert(0);
                *total_count += nb_min;
                let count_per_min = sleeps_per_guard_per_min
                    .entry(guard)
                    .or_insert_with(HashMap::new);
                for min in start.minute..start.minute + nb_min {
                    let count = count_per_min.entry(min).or_insert(0);
                    *count += 1;
                    let count = sleeps_per_guard_and_min.entry((guard, min)).or_insert(0);
                    *count += 1;
                }
            }
        }
    }
    if is_part1 {
        let guard = sleeps_total.iter().max_by_key(|entry| entry.1).unwrap().0;
        let minute = sleeps_per_guard_per_min[guard]
            .iter()
            .max_by_key(|entry| entry.1)
            .unwrap()
            .0;
        guard * minute
    } else {
        let (guard, minute) = sleeps_per_guard_and_min
            .iter()
            .max_by_key(|entry| entry.1)
            .unwrap()
            .0;
        guard * minute
    }
}

fn part1(events: &InputContent) -> Int {
    find_sleeping_guard(events, true)
}

fn part2(events: &InputContent) -> Int {
    find_sleeping_guard(events, false)
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

    const EXAMPLE: &str = "[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up";
    #[test]
    fn test_action_from_str() {
        assert_eq!(Action::from_str("wakes up"), Ok(Action::WakesUp));
        assert_eq!(Action::from_str("falls asleep"), Ok(Action::FallsAsleep));
        assert_eq!(
            Action::from_str("Guard #99 begins shift"),
            Ok(Action::ShiftBegins(99))
        );
    }
    #[test]
    fn test_timestamp_from_str() {
        assert_eq!(
            Timestamp::from_str("[1518-11-05 00:55"),
            Ok(Timestamp {
                year: 1518,
                month: 11,
                day: 5,
                hour: 0,
                minute: 55,
            })
        );
    }
    #[test]
    fn test_event_from_str() {
        assert_eq!(
            Event::from_str("[1518-11-05 00:03] Guard #99 begins shift"),
            Ok(Event {
                timestamp: Timestamp {
                    year: 1518,
                    month: 11,
                    day: 5,
                    hour: 0,
                    minute: 3,
                },
                action: Action::ShiftBegins(99,),
            },)
        );
    }

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE)), 240);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 4455);
    }
}
