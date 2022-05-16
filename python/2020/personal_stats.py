import re
import datetime

header = """      --------Part 1--------   --------Part 2--------
Day       Time   Rank  Score       Time   Rank  Score"""
new_header = """      --------Part 1--------   --------Part 2--------  --------Delta--------
Day       Time   Rank  Score       Time   Rank  Score       Delta rank  Delta time"""


stats = """
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
"""


print(new_header)
time_re = r"([0-9:]+|>24h)"
stat_line_re = re.compile(
    r"^\s+(?P<day>\d+)\s+(?P<time1>%s)\s+(?P<rank1>\d+)\s+(?P<score1>\d+)\s+(?P<time2>%s)\s+(?P<rank2>\d+)\s+(?P<score2>\d+)$"
    % (time_re, time_re)
)
time_format = "%H:%M:%S"
for line in stats.split("\n"):
    if line:
        m = stat_line_re.match(line)
        d = m.groupdict()
        rank1 = int(d["rank1"])
        rank2 = int(d["rank2"])
        dtime1 = d["time1"]
        dtime2 = d["time2"]
        if dtime2 == ">24h":
            dtime2 = "23:59:59"
        time1 = datetime.datetime.strptime(dtime1, time_format)
        time2 = datetime.datetime.strptime(dtime2, time_format)
        delta_rank = rank1 - rank2
        delta_time = time2 - time1
        print("{}       {:5d}        {}".format(line, delta_rank, delta_time))
