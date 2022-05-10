set -x

# Retrieve date
real_day=$(date "+%-d")
real_year=$(date "+%Y")

# Get date used based on user parameters and default to current day
day="${1:-$real_day}"
year="${2:-$real_year}"

folder="${year}/day${day}"
bin="day${day}_${year}"
src_file="src/${folder}/main.rs"

# Instruction for Cargo content:
echo """Add the following content to Cargo.toml:
[[bin]]
name = \"${bin}\"
path = \"${src_file}\"
"""

# Prepare folders
mkdir -p {res,src}/${folder}

# Use template files
input_file="res/${folder}/input.txt"
input_example="res/template/input.txt"
cp "${input_example}" "${input_file}"
cp src/template/main.rs "${src_file}"

# Update code
sed -i "s#${input_example}#${input_file}#g" "${src_file}"

# Instruction to run cargo
echo """cargo run --bin "${bin}""""
