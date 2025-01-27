#set -x
set -e

# Retrieve date
real_day=$(date "+%-d")
real_year=$(date "+%Y")

# Get date used based on user parameters and default to current day
day="${1:-$real_day}"
year="${2:-$real_year}"

# Configuration
browser="${aoc_browser:-}"   # For example: '' or 'firefox'
editor="${aoc_editor:-}"     # For example: '' or 'vim'

get_input="1"
overwrite_input="0"

get_puzzle="1"
overwrite_puzzle="1"
extract_answers="1"

get_stats="1"
overwrite_stats="1"

create_rust="1"
overwrite_rust="0"

create_python="1"
overwrite_python="0"

generate_readme="1"
git_add="1"
git_commit="1"

# URLs
puzzle_url="https://adventofcode.com/${year}/day/${day}"
input_url="https://adventofcode.com/${year}/day/${day}/input"
stats_url="https://adventofcode.com/${year}/leaderboard/self"

# Move to correct directory
cd "$(dirname "$0")"

# Check workspace status
if [ "${git_add}" = "1" ] && [ -n "$(git status --porcelain)" ];
then
	git status
	git_add="0"
	echo "Git workspace is not clean - git commands will be skipped"
fi

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

# Paths
puzzle_file="resources/year${year}_day${day}_puzzle.html"
input_file="resources/year${year}_day${day}_input.txt"
answer_file="resources/year${year}_day${day}_answer.txt"
stats_file="misc/leaderboard_self_${year}.html"
python_script_file="python/${year}/day${day}.py"
rust_src_file_rel="src/${year}/day${day}.rs"
rust_src_file="rust/${rust_src_file_rel}"
cargo_file="rust/Cargo.toml"
readme_file="README.md"

files_to_open_in_editor=()

# Get input file
get_url_and_save() {
	url="${1}"
	dest="${2}"
	overwrite="${3}"
	cleanup="${4}"
	# files_to_open_in_editor+=("${dest}")
	# echo "About to save ${url} in ${dest}"
	mkdir -p $(dirname "${dest}")
	if [ "${overwrite}" == "0" -a -f "${dest}" ]; then
		echo "File ${dest} already exists - ignored."
	elif [ -z "${AOC_SESSION_COOKIE}" ]; then
		# Create empty file
		touch "${dest}"
		echo "Empty file ${dest} created"
	else
		# echo "Cookie session AOC_SESSION_COOKIE used to get file at url ${url}"
		# Get file
		curl -s "${url}" -H "cookie: session=${AOC_SESSION_COOKIE}" -o "${dest}"
		if [ "${cleanup}" == "1" ]; then
			# Lines that keep changing (and are not so relevant)
			sed -i '/div id="sponsor"/d' "${dest}"  # Random sponsor
			sed -i '/class="title-global"/d' "${dest}"  # Random header, stars count
		fi
		echo "Url ${url} saved in ${dest}"
	fi
}

if [ "${get_puzzle}" = "1" ]; then
	get_url_and_save "${puzzle_url}" "${puzzle_file}" "${overwrite_puzzle}" "1"
fi
if [ "${get_stats}" = "1" ]; then
	get_url_and_save "${stats_url}" "${stats_file}" "${overwrite_stats}" "1"
fi
if [ "${get_input}" = "1" ]; then
	get_url_and_save "${input_url}" "${input_file}" "${overwrite_input}" "0"
fi
if [ "${extract_answers}" = "1" ]; then
	sed -n "s/<p>Your puzzle answer was <code>\([^<]*\)<\/code>\..*/\1/gp" "${puzzle_file}" | tee "${answer_file}"
fi

create_code_from_template() {
	template="${1}"
	dest="${2}"
	overwrite="${3}"

	files_to_open_in_editor+=("${dest}")
	if [ "${overwrite}" == "0" -a -f "${dest}" ]; then
		echo "Script file ${dest} already exists - ignored."
		return
	fi

	# Create folder
	mkdir -p $(dirname "${dest}")
	# Create script file based on template
	cp "${template}" "${dest}"
	# Update file examples used
	input_example="resources/yearYYYY_dayDD_input.txt"
	answer_example="resources/yearYYYY_dayDD_answer.txt"
	sed -i "s#${input_example}#${input_file}#g" "${dest}"
	sed -i "s#${answer_example}#${answer_file}#g" "${dest}"
}

# Count lines in input files to use the most relevant template
nb_lines="$(cat "${input_file}" | wc -l)"

# Create Python file
if [ "${create_python}" = "1" ]; then
	case "${nb_lines}" in
		0|1) python_template="python/template_one_line.py";;
		*)   python_template="python/template_multi_line.py";;
	esac
	create_code_from_template "${python_template}" "${python_script_file}" "${overwrite_python}"
	echo "Run Python solution with 'python3 ${python_script_file}'"
fi

# Create Rust file
if [ "${create_rust}" = "1" ]; then
	rust_bin="${year}_day${day}"
	case "${nb_lines}" in
		0|1) rust_template="rust/src/templates/template_one_line.rs";;
		*)   rust_template="rust/src/templates/template_multi_line.rs";;
	esac

	# Add content in Cargo.toml file
	cargo_content="[[bin]]\nname = \"${rust_bin}\"\npath = \"${rust_src_file_rel}\"\n\n"
	# echo -e "Add the following content to ${cargo_file}:\n${cargo_content}"
	grep -q "${rust_bin}" "${cargo_file}" || sed -i "s#.*See more keys#${cargo_content}&#g" "${cargo_file}"

	create_code_from_template "${rust_template}" "${rust_src_file}" "${overwrite_rust}"
	echo "Run Rust solution with './rust/one_day.sh ${day} ${year}' or '(cd rust && cargo run --bin "${rust_bin}")'"
fi

# Generate README
if [ "${generate_readme}" = "1" ]; then
	python3 generate_readme.py "${readme_file}"
fi

# Add to git
if [ "${git_add}" = "1" ]; then
	git status
	git add "${puzzle_file}" "${input_file}" "${answer_file}" "${stats_file}" "${python_script_file}" "${rust_src_file}" "${cargo_file}" "${readme_file}"
	git status
	commit_title="Year ${year} - Day ${day} - Getting started"
	if [ "${git_commit}" = "1" ]; then
	   git commit -m "${commit_title}"
	else
	   echo "Commit with: 'git commit -m \"${commit_title}\"'"
	fi
fi

# Open files in editor
if [ -z "${editor}" ]; then
	echo "No editor set to open ${files_to_open_in_editor[@]} - ignored."
else
	"${editor}" "${files_to_open_in_editor[@]}"
fi
