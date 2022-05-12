set -x
set -e

# Retrieve date
real_day=$(date "+%-d")
real_year=$(date "+%Y")

# Get date used based on user parameters and default to current day
day="${1:-$real_day}"
year="${2:-$real_year}"

# Binary name
bin="day${day}_${year}"

# Run cargo commands
cargo test --bin "${bin}"
cargo run --bin "${bin}"
cargo clippy
