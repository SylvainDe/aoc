use common::input::collect_from_lines;
use common::input::get_file_content;
use core::str::FromStr;
use lazy_static::lazy_static;
use regex::Regex;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2018_day4_input.txt";

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

#[derive(Debug, Eq, Ord, PartialEq, PartialOrd)]
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
        lazy_static! {
            static ref RE: Regex = Regex::new(
                r"^\[(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+) (?P<hour>\d+):(?P<minute>\d+)"
            )
            .unwrap();
        }
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
            timestamp: ts.parse().map_err(|_| {})?,
            action: action.parse().map_err(|_| {})?,
        })
    }
}
type InputContent = Vec<Event>;

fn get_input_from_str(string: &str) -> InputContent {
    let mut entries = collect_from_lines(string);
    entries.sort();
    entries
}

fn part1(events: &InputContent) -> Int {
    for _e in events {}
    0
}

#[allow(clippy::trivially_copy_pass_by_ref, clippy::missing_const_for_fn)]
fn part2(_arg: &InputContent) -> Int {
    0
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_str(&get_file_content(INPUT_FILEPATH));
    let res = part1(&data);
    println!("{:?}", res);
    assert_eq!(res, 0);
    let res2 = part2(&data);
    println!("{:?}", res2);
    assert_eq!(res2, 0);
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
        assert_eq!(part1(&get_input_from_str(EXAMPLE)), 0);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 0);
    }
}
