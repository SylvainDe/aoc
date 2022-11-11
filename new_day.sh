#set -x
set -e

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
overwrite_input="0"

get_puzzle="1"
overwrite_puzzle="1"

create_rust="1"
overwrite_rust="0"

create_python="1"
overwrite_python="0"

generate_readme="1"
git_add="1"

# URLs
puzzle_url="https://adventofcode.com/${year}/day/${day}"
input_url="https://adventofcode.com/${year}/day/${day}/input"

# Move to correct directory
cd "$(dirname "$0")"

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
puzzle_file="resources/year${year}_day${day}_puzzle.txt"
input_file="resources/year${year}_day${day}_input.txt"
python_script_file="python/${year}/day${day}.py"
rust_src_file_rel="src/${year}/day${day}/main.rs"
rust_src_file="rust/${rust_src_file_rel}"
cargo_file="rust/Cargo.toml"
readme_file="README.md"

# Get input file
get_url_and_save() {
	url="${1}"
	dest="${2}"
	overwrite="${3}"
	cleanup="${4}"
	echo "About to save ${url} in ${dest}"
	mkdir -p $(dirname "${dest}")
	if [ "${overwrite}" == "0" -a -f "${dest}" ]; then
		echo "File ${dest} already exists - ignored."
	elif [ -z "${AOC_SESSION_COOKIE}" ]; then
		# Create empty file
		touch "${dest}"
	else
		echo "Cookie session AOC_SESSION_COOKIE used to get file at url ${url}"
		# Get file
		curl "${url}" -H "cookie: session=${AOC_SESSION_COOKIE}" -o "${dest}"
		if [ "${cleanup}" == "1" ]; then
			# Lines that keep changing (and are not so relevant)
			sed -i '/div id="sponsor"/d' "${dest}"  # Random sponsor
			sed -i '/class="title-global"/d' "${dest}"  # Random header, stars count
		fi
	fi
}

if [ "${get_puzzle}" = "1" ]; then
	get_url_and_save "${puzzle_url}" "${puzzle_file}" "${overwrite_puzzle}" "1"
fi
if [ "${get_input}" = "1" ]; then
	get_url_and_save "${input_url}" "${input_file}" "${overwrite_input}" "0"
fi

create_code_from_template() {
	template="${1}"
	dest="${2}"
	overwrite="${3}"

	if [ "${overwrite}" == "0" -a -f "${dest}" ]; then
		echo "Script file ${dest} already exists - ignored."
		return
	fi

	# Create folder
	mkdir -p $(dirname "${dest}")
	# Create script file based on template
	cp "${template}" "${dest}"
	# Update file example used
	input_example="resources/yearYYYY_dayDD_input.txt"
	sed -i "s#${input_example}#${input_file}#g" "${dest}"
}

open_file_in_editor() {
	filename="${1}"
	if [ -z "${editor}" ]; then
		echo "No editor set - ignored."
	else
		"${editor}" "${filename}"
	fi
}

# Create Python file
if [ "${create_python}" = "1" ]; then
	python_template="python/day_template.py"
	create_code_from_template "${python_template}" "${python_script_file}" "${overwrite_python}"
	open_file_in_editor "${python_script_file}"
fi

# Create Rust file
if [ "${create_rust}" = "1" ]; then
	rust_bin="day${day}_${year}"
	rust_template="rust/src/template/main.rs"

	# Add content in Cargo.toml file
	cargo_content="[[bin]]\nname = \"${rust_bin}\"\npath = \"${rust_src_file_rel}\"\n\n"
	echo -e "Add the following content to ${cargo_file}:\n${cargo_content}"
	grep "${rust_bin}" "${cargo_file}" || sed -i "s#.*See more keys#${cargo_content}&#g" "${cargo_file}"

	create_code_from_template "${rust_template}" "${rust_src_file}" "${overwrite_rust}"

	# Instruction to run cargo
	echo """(cd rust && cargo run --bin "${rust_bin}")"""

	open_file_in_editor "${rust_src_file}"
fi

# Generate README
if [ "${generate_readme}" = "1" ]; then
	python3 generate_readme.py > "${readme_file}"
fi

# Add to git
if [ "${git_add}" = "1" ]; then
	git status
	# TODO: Some files may be created in a new folder which needs to be added
	# as well. Other files should not have their folder added automatically.
	for f in "${puzzle_file}" "${input_file}" "${python_script_file}" "${rust_src_file}" "${cargo_file}" "${readme_file}"; do
		echo "${f} not done yet"
		# git add "${f}"
	done
	git status
fi
