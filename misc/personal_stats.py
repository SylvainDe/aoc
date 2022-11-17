import re
import datetime

header = """
            --------Part 1--------    --------Part 2--------     --------Delta--------
Year Day       Time   Rank  Score        Time   Rank  Score       Delta rank  Delta time"""


# TODO: Extract directly from HTML files
all_stats = {
    # From https://adventofcode.com/2015/leaderboard/self
    "2015": """
 20       >24h   7420      0          -      -      -
 17       >24h   9066      0       >24h   8893      0
 14       >24h  11564      0       >24h  10783      0
 10       >24h  14915      0       >24h  14338      0
  9       >24h  13858      0       >24h  13562      0
  8       >24h  16030      0       >24h  15108      0
  7       >24h  16977      0       >24h  16356      0
  6       >24h  24502      0       >24h  23373      0
  5       >24h  30899      0       >24h  26132      0
  4       >24h  31816      0       >24h  30514      0
  3       >24h  38096      0       >24h  34845      0
  2       >24h  46794      0       >24h  41895      0
  1       >24h  73958      0       >24h  59590      0
""",
    # From https://adventofcode.com/2016/leaderboard/self
    "2016": """
 23       >24h   4419      0       >24h   4171      0
 22       >24h   4602      0          -      -      -
 20       >24h   5262      0       >24h   5035      0
 19       >24h   5981      0          -      -      -
 18       >24h   5355      0       >24h   5316      0
 17       >24h   4931      0       >24h   4819      0
 16       >24h   6308      0       >24h   6134      0
 15       >24h   5660      0       >24h   5620      0
 14       >24h   6347      0       >24h   6094      0
 13       >24h   5945      0       >24h   5682      0
 12       >24h   7561      0       >24h   7468      0
 10       >24h   8021      0       >24h   7886      0
  9       >24h  10673      0       >24h   9100      0
  8       >24h  10753      0       >24h  10554      0
  7       >24h  13144      0       >24h  11818      0
  6       >24h  15055      0       >24h  14623      0
  5       >24h  14810      0       >24h  14144      0
  4       >24h  14988      0       >24h  14162      0
  3       >24h  18736      0       >24h  16690      0
  2       >24h  20037      0       >24h  17792      0
  1       >24h  25876      0       >24h  19956      0
""",
    # From https://adventofcode.com/2017/leaderboard/self
    "2017": """
  7       >24h  22679      0       >24h  17767      0
  4       >24h  32621      0       >24h  29278      0
  3       >24h  34223      0       >24h  25371      0
  2       >24h  48833      0       >24h  41569      0
  1       >24h  59263      0       >24h  49329      0
""",
    # From https://adventofcode.com/2018/leaderboard/self
    "2018": """
  8       >24h  19646      0       >24h  18584      0
  7       >24h  23458      0       >24h  19208      0
  5       >24h  34168      0       >24h  32893      0
  3       >24h  46711      0       >24h  44250      0
  2       >24h  64240      0       >24h  57387      0
  1       >24h  93132      0       >24h  72774      0
""",
    # From https://adventofcode.com/2019/leaderboard/self
    "2019": """
 24       >24h    6072      0       >24h    4709      0
 22       >24h    6835      0          -       -      -
 20       >24h    5763      0       >24h    5009      0
 18       >24h    5490      0          -       -      -
 14       >24h   12418      0       >24h   11485      0
 12       >24h   18344      0       >24h   14713      0
 10       >24h   21075      0       >24h   17866      0
  9       >24h   21964      0       >24h   21857      0
  8       >24h   29605      0       >24h   28440      0
  6       >24h   35735      0       >24h   33794      0
  5       >24h   38629      0       >24h   36873      0
  4       >24h   56951      0       >24h   52500      0
  3       >24h   57359      0       >24h   50261      0
  2       >24h   86926      0       >24h   78440      0
  1       >24h  118511      0       >24h  103841      0
""",
    # From https://adventofcode.com/2020/leaderboard/self
    "2020": """
 25   15:47:10  10667      0   15:47:57   7954      0
 24   12:56:48  10470      0       >24h  11576      0
 23   08:31:21   8665      0   10:12:42   5593      0
 22   02:43:14   5936      0   03:22:28   4227      0
 21   15:53:45  10730      0   15:58:12  10412      0
 20   12:44:22   9035      0       >24h   7877      0
 19   05:31:17   5888      0   08:24:36   5242      0
 18   04:00:44   7658      0   04:19:16   6330      0
 17   02:40:38   5423      0   02:48:40   4980      0
 16   03:08:50   9470      0   04:16:59   7080      0
 15   02:56:01   9703      0   03:02:25   8247      0
 14   03:26:04   9893      0   04:16:02   7838      0
 13   01:57:08   8651      0   02:34:13   3935      0
 12   03:51:56  11266      0   04:07:28   9347      0
 11   02:20:42   8833      0   02:46:37   7158      0
 10   03:09:23  16635      0   07:32:15  15346      0
  9   02:35:35  14408      0   02:46:41  13079      0
  8   03:05:11  16551      0   03:25:06  13837      0
  7   05:57:16  18664      0   06:07:51  15021      0
  6   09:37:37  36350      0   09:44:54  33848      0
  5   03:16:34  14519      0   03:21:16  13611      0
  4   02:17:37  14475      0   02:58:30  11542      0
  3   03:06:56  17982      0   03:18:47  16885      0
  2   02:53:45  15724      0   03:08:50  15256      0
  1   15:30:58  57284      0   15:41:05  53086      0
""",
    # From https://adventofcode.com/2021/leaderboard/self
    "2021": """
 25       >24h  13317      0          -      -      -
 23       >24h   9695      0          -      -      -
 22   02:50:38   5979      0          -      -      -
 21   02:44:55   7303      0   05:42:55   5714      0
 20   03:45:32   5536      0   03:48:22   5269      0
 19       >24h  11385      0       >24h  11187      0
 18   14:40:34   9669      0   14:44:29   9401      0
 17   11:18:06  16664      0   12:10:27  15594      0
 16   04:33:38   7402      0   04:44:22   6315      0
 15   03:12:31   8633      0   03:26:18   6174      0
 14   05:13:50  20030      0   05:31:18  12343      0
 13   01:02:52   6605      0   01:05:55   5617      0
 12   02:54:25   8873      0   03:10:03   7849      0
 11   03:54:37  12089      0   03:57:19  11826      0
 10   02:27:19  14176      0   02:37:21  12849      0
  9   03:30:47  19647      0   04:20:07  14360      0
  8   07:04:15  32138      0   07:11:28  17799      0
  7   03:03:46  22436      0   03:21:14  21508      0
  6   03:08:19  20459      0   03:19:52  15283      0
  5   02:57:27  13036      0   03:09:47  11538      0
  4   06:15:23  21870      0   06:27:32  19726      0
  3   08:16:54  54746      0   08:32:17  35746      0
  2   07:50:32  56717      0   07:52:32  53147      0
  1   07:35:16  44355      0   07:40:40  38014      0
""",
    # From https://adventofcode.com/2022/leaderboard/self
    "2022": """
""",
}


print(header)
time_re = r"([0-9:]+|>24h)"
stat_line_re = re.compile(
    r"^\s+(?P<day>\d+)\s+(?P<time1>%s)\s+(?P<rank1>\d+|-)\s+(?P<score1>\d+)\s+(?P<time2>%s|-)\s+(?P<rank2>\d+|-)\s+(?P<score2>\d+|-)$"
    % (time_re, time_re)
)
time_format = "%H:%M:%S"
for year, stats in all_stats.items():
    for line in reversed(stats.split("\n")):
        if line:
            m = stat_line_re.match(line)
            if m is None:
                continue  # TODO
            d = m.groupdict()
            rank1 = d["rank1"]
            rank2 = d["rank2"]
            dtime1 = d["time1"]
            dtime2 = d["time2"]
            assert (rank2 == "-") == (dtime2 == "-")
            if rank2 == "-":
                delta_rank = "    -"
                delta_time = "      -"
            else:
                if dtime1 == ">24h":
                    dtime1 = "23:59:59"
                if dtime2 == ">24h":
                    dtime2 = "23:59:59"
                time1 = datetime.datetime.strptime(dtime1, time_format)
                time2 = datetime.datetime.strptime(dtime2, time_format)
                delta_rank = "{:5d}".format(int(rank1) - int(rank2))
                delta_time = time2 - time1
            print("{} {}       {}        {}".format(year, line, delta_rank, delta_time))