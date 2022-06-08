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

# Paths and filenames
bin="day${day}_${year}"
src_folder="src/${year}/day${day}"
src_file="${src_folder}/main.rs"
input_file="../resources/year${year}_day${day}_input.txt"
src_example="src/template/main.rs"
input_example="../resources/yearYYYY_dayDD_input.txt"

# Add content in Cargo.toml file
cargo_file="Cargo.toml"
cargo_content="[[bin]]\nname = \"${bin}\"\npath = \"${src_file}\"\n\n"
echo -e "Add the following content to ${cargo_file}:\n${cargo_content}"
sed -i "s#.*See more keys#${cargo_content}&#g" "${cargo_file}"

# Prepare folder
mkdir -p "${src_folder}"

# Optional: read cookie config file - setting AOC_SESSION_COOKIE env variable
# See template file aoc_cookie_session.sh for instructions
source ~/aoc_cookie_session.sh 2> /dev/null

# Get input file
if [ -f "${input_file}" ]; then
    echo "Input file ${input_file} already exists - ignored."
elif [ -z "${AOC_SESSION_COOKIE}" ]; then
    # Use template input file
    cp "${input_example}" "${input_file}"
else
    echo "Cookie session AOC_SESSION_COOKIE used to get input file."
    # Get input file
    curl "${input_url}" -H "cookie: session=${AOC_SESSION_COOKIE}" -o "${input_file}"
fi

# Create code file based on template
if [ -f "${src_file}" ]; then
    echo "Code file ${src_file} already exists - ignored."
else
	cp "${src_example}" "${src_file}"
	sed -i "s#${input_example}#${input_file}#g" "${src_file}"
fi

# Instruction to run cargo
echo """cargo run --bin "${bin}""""

# Open relevant files to start solving the problem
if [ -z "${editor}" ]; then
    echo "No editor set - ignored."
else
    "${editor}" "${src_file}" "${input_file}"
fi
