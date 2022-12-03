use common::input::collect_from_lines;
use common::input::get_file_content;
use core::str::FromStr;
use lazy_static::lazy_static;
use regex::Regex;
use std::cmp::max;
use std::cmp::min;
use std::collections::HashSet;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2021_day22_input.txt";

type Int = i32;

#[derive(Debug, PartialEq)]
struct Instruction {
    on: bool,
    x1: Int,
    x2: Int,
    y1: Int,
    y2: Int,
    z1: Int,
    z2: Int,
}

impl FromStr for Instruction {
    type Err = ();
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        // on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
        lazy_static! {
            static ref RE: Regex = Regex::new(concat!(
                r"^(?P<action>on|off) ",
                r"x=(?P<x1>-?\d+)\.\.(?P<x2>-?\d+),",
                r"y=(?P<y1>-?\d+)\.\.(?P<y2>-?\d+),",
                r"z=(?P<z1>-?\d+)\.\.(?P<z2>-?\d+)$"
            ))
            .unwrap();
        }
        let c = RE.captures(s).ok_or(())?;
        let get_field = |s: &str| c.name(s).ok_or(());
        let to_int = |s: &str| get_field(s)?.as_str().parse::<Int>().map_err(|_| {});
        Ok(Self {
            on: get_field("action")?.as_str() == "on",
            x1: to_int("x1")?,
            x2: to_int("x2")?,
            y1: to_int("y1")?,
            y2: to_int("y2")?,
            z1: to_int("z1")?,
            z2: to_int("z2")?,
        })
    }
}

type InputContent = Vec<Instruction>;

fn get_input_from_str(string: &str) -> InputContent {
    collect_from_lines(string)
}

fn perform_instructions_naive(instructions: &InputContent) -> usize {
    let mut cubes = HashSet::new();
    for Instruction {
        on,
        x1,
        x2,
        y1,
        y2,
        z1,
        z2,
    } in instructions
    {
        let (x_min, x_max) = (max(*x1, -50), min(*x2, 50));
        let (y_min, y_max) = (max(*y1, -50), min(*y2, 50));
        let (z_min, z_max) = (max(*z1, -50), min(*z2, 50));
        for x in x_min..=x_max {
            for y in y_min..=y_max {
                for z in z_min..=z_max {
                    let c = (x, y, z);
                    if *on {
                        cubes.insert(c);
                    } else {
                        cubes.remove(&c);
                    }
                }
            }
        }
    }
    cubes.len()
}

#[allow(clippy::missing_const_for_fn)]
fn _perform_instructions_optimised(_instructions: &InputContent) -> usize {
    // A possible and logical optimisation is not to keep track of individual
    // cubes but instead track of cuboids as large as possible.
    // The main issue is computing sum/differences of cuboids.
    // Note:
    //  - The idea is to split cuboids into disjoints smaller cuboids such
    // the operations are trivial.
    //  - the initial logic is about both sum and differences but
    // the analysis can be limited to differences: to compute A + B, one can
    // compute: (A - B) (the sub-cuboids of A disjoint from B) and then add B
    // (this may not be fully optimal as it may lead to more splits than needed
    // but this is probably good enough)
    //  - it is probably logic easier to work with [close, open) ranges rather
    // than [close, close] (see https://fhur.me/posts/always-use-closed-open-intervals)
    //
    // Lets's see how things work in 2D: _split_1d.
    0
}

const fn value_in_range(val: Int, x: Int, y: Int) -> bool {
    x <= val && val < y
}

fn _split_1d(x1: Int, x2: Int, y1: Int, y2: Int) -> Vec<(Int, Int, bool, bool)> {
    // Return list of disjoint sets with a boolean to know whether the chunk
    // belong to x or y
    // dbg!(x1, x2, y1, y2);
    assert!(x1 <= x2);
    assert!(y1 <= y2);
    let mut ret = Vec::<(Int, Int, bool, bool)>::new();
    let mut points = vec![x1, x2, y1, y2];
    points.sort_unstable();
    for win in points.windows(2) {
        let (a, b) = (win[0], win[1]);
        if a < b {
            let in_x = value_in_range(a, x1, x2);
            let in_y = value_in_range(a, y1, y2);
            if in_x || in_y {
                ret.push((a, b, in_x, in_y));
            }
        }
    }
    ret
}

fn part1(instructions: &InputContent) -> usize {
    perform_instructions_naive(instructions)
}

#[allow(clippy::missing_const_for_fn)]
fn part2(_arg: &InputContent) -> Int {
    0
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_str(&get_file_content(INPUT_FILEPATH));
    let res = part1(&data);
    println!("{:?}", res);
    assert_eq!(res, 503_864);
    let res2 = part2(&data);
    println!("{:?}", res2);
    assert_eq!(res2, 0);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE: &str = "on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10";

    const EXAMPLE2: &str = "on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682";

    const EXAMPLE3: &str = "on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507";

    #[test]
    fn test_foobar_from_str() {
        assert!(Instruction::from_str("").is_err());
        assert_eq!(
            Instruction::from_str("on x=10..12,y=11..13,z=15..16"),
            Ok(Instruction {
                on: true,
                x1: 10,
                x2: 12,
                y1: 11,
                y2: 13,
                z1: 15,
                z2: 16,
            })
        );
    }

    #[test]
    fn test_split_1d() {
        // Disjoint
        assert_eq!(
            _split_1d(1, 3, 4, 6),
            vec![(1, 3, true, false,), (4, 6, false, true,),]
        );
        assert_eq!(
            _split_1d(1, 4, 4, 6),
            vec![(1, 4, true, false,), (4, 6, false, true,),]
        );
        assert_eq!(
            _split_1d(4, 6, 1, 3),
            vec![(1, 3, false, true,), (4, 6, true, false,),]
        );
        // Full overlap
        assert_eq!(
            _split_1d(1, 6, 2, 5),
            vec![
                (1, 2, true, false,),
                (2, 5, true, true,),
                (5, 6, true, false,),
            ]
        );
        assert_eq!(
            _split_1d(2, 5, 1, 6),
            vec![
                (1, 2, false, true,),
                (2, 5, true, true,),
                (5, 6, false, true,),
            ]
        );
        // Partial overlap
        assert_eq!(
            _split_1d(1, 6, 3, 8),
            vec![
                (1, 3, true, false,),
                (3, 6, true, true,),
                (6, 8, false, true,),
            ]
        );
        assert_eq!(
            _split_1d(3, 8, 1, 6),
            vec![
                (1, 3, false, true,),
                (3, 6, true, true,),
                (6, 8, true, false,),
            ]
        );
        // Edge cases ?
    }

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE)), 39);
        assert_eq!(part1(&get_input_from_str(EXAMPLE2)), 590784);
        assert_eq!(part1(&get_input_from_str(EXAMPLE3)), 474140);
    }
    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE3)), 0);
    }
}
