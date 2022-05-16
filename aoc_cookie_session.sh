# Instructions to get the session cookie (based on https://github.com/GreenLightning/advent-of-code-downloader )
#
# How Do I Get My Session Cookie?
#
# Google Chrome:
#
#     Go to adventofcode.com
#     Make sure you are logged in
#     Right click and select "Inspect"
#     Select the "Application" tab
#     In the tree on the left, select "Storage" → "Cookies" → "https://adventofcode.com"
#     You should see a table of cookies, find the row with "session" as name
#     Double click the row in the "Value" column to select the value of the cookie
#     Press CTRL + C or right click and select "Copy" to copy the cookie
#     Paste it into your configuration file or on the command line
#
# Mozilla Firefox:
#
#     Go to adventofcode.com
#     Make sure you are logged in
#     Right click and select "Inspect Element"
#     Select the "Storage" tab
#     In the tree on the left, select "Cookies" → "https://adventofcode.com"
#     You should see a table of cookies, find the row with "session" as name
#     Double click the row in the "Value" column to select the value of the cookie
#     Press CTRL + C or right click and select "Copy" to copy the cookie
#     Paste it into your configuration file or on the command line

#AOC_SESSION_COOKIE="<your_value_here>"
#echo "AOC_SESSION_COOKIE=${AOC_SESSION_COOKIE}"
