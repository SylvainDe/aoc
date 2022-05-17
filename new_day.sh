set -x

# Retrieve date
real_day=$(date "+%-d")
real_year=$(date "+%Y")

# Get date used based on user parameters and default to current day
day="${1:-$real_day}"
year="${2:-$real_year}"

# Configuration
browser="firefox"  # Can be left empty
editor="vim"  # Can be left empty
browser=""
editor=""
get_input="1"
get_puzzle="1"
create_rust="0"
create_python="0"

# URLs
puzzle_url="https://adventofcode.com/${year}/day/${day}"
input_url="https://adventofcode.com/${year}/day/${day}/input"

# Open pages
if [ -z "${browser}" ]; then
    echo "No browser set - ignored."
else
    "${browser}" "${puzzle_url}"
    "${browser}"  "${input_url}"
fi


# Optional: read cookie config file - setting AOC_SESSION_COOKIE env variable
# See template file aoc_cookie_session.sh for instructions
source ~/aoc_cookie_session.sh 2> /dev/null

# Get input file
input_file="resources/year${year}_day${day}_input.txt"
puzzle_file="resources/year${year}_day${day}_puzzle.txt"

get_url_and_save() {
	url="${1}"
	dest="${2}"
    echo "${url} - ${dest}"
	mkdir -p $(dirname "${dest}")
	if [ -f "${dest}" ]; then
		echo "File ${dest} already exists - ignored."
	elif [ -z "${AOC_SESSION_COOKIE}" ]; then
		# Create empty file
		touch "${dest}"
	else
		echo "Cookie session AOC_SESSION_COOKIE used to get file."
		# Get file
		curl "${url}" -H "cookie: session=${AOC_SESSION_COOKIE}" -o "${dest}"
	fi


}

if [ "${get_puzzle}" = "1" ]; then
	get_url_and_save "${puzzle_url}" "${puzzle_file}"
fi
if [ "${get_input}" = "1" ]; then
	get_url_and_save "${input_url}" "${input_file}"
fi

# TODO: Perform actions for Rust and/or Python
if [ "${create_rust}" = "1" ]; then
    echo "Not implemented yet"
fi
if [ "${create_python}" = "1" ]; then
    echo "Not implemented yet"
fi
