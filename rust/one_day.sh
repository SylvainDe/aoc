set -x
set -e

# Retrieve date
real_day=$(date "+%-d")
real_year=$(date "+%Y")

# Get date used based on user parameters and default to current day
day="${1:-$real_day}"
year="${2:-$real_year}"

# Paths and filenames
bin="day${day}_${year}"

# Run cargo commands
cargo test --lib
cargo test --bin "${bin}"
cargo run --bin "${bin}"
cargo clippy --bin "${bin}" -- \
    -D clippy::all \
    -D clippy::correctness \
    -D clippy::suspicious \
    -D clippy::style \
    -D clippy::complexity \
    -D clippy::perf \
    -D clippy::pedantic \
    -D clippy::cargo \
    -D clippy::nursery
cargo fmt --check

