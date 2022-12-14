set -x
set -e

# Retrieve date
real_day=$(date "+%-d")
real_year=$(date "+%Y")

# Get date used based on user parameters and default to current day
day="${1:-$real_day}"
year="${2:-$real_year}"

# Option to fix things automatically (at your own risk)
autofix="1"
fix_options="--allow-dirty --allow-staged"

# Bin name
bin="${year}_day${day}"

# Clippy options
clippy_checks="-D clippy::all
-D clippy::correctness
-D clippy::suspicious
-D clippy::style
-D clippy::complexity
-D clippy::perf
-D clippy::pedantic
-D clippy::cargo
-D clippy::nursery
-D clippy::restriction
-A clippy::indexing_slicing
-A clippy::integer_arithmetic
-A clippy::modulo_arithmetic
-A clippy::default_numeric_fallback
-A clippy::implicit_return
-A clippy::missing_inline_in_public_items
-A clippy::unwrap_used
-A clippy::expect_used
-A clippy::missing_docs_in_private_items
-A clippy::pattern_type_mismatch
-A clippy::exhaustive_enums
-A clippy::exhaustive_structs
-A clippy::map_err_ignore
-A clippy::as_conversions
-A clippy::shadow_reuse
-A clippy::shadow_unrelated
-A clippy::shadow_same
-A clippy::else_if_without_else
-A clippy::use_debug
-A clippy::panic
-A clippy::print_stdout
-A clippy::integer_division
-A clippy::string_slice"

# Run cargo commands
if [ "${autofix}" = "1" ]; then
    cargo fix ${fix_options} --lib
    cargo fix ${fix_options} --bin "${bin}"
fi
cargo test --lib
cargo test --bin "${bin}" -- --nocapture --test-threads=1
cargo run --bin "${bin}"
if [ "${autofix}" = "1" ]; then
    cargo clippy --fix ${fix_options} --lib          -- ${clippy_checks}
    cargo clippy --fix ${fix_options} --bin "${bin}" -- ${clippy_checks}
fi
cargo clippy --lib          -- ${clippy_checks}
cargo clippy --bin "${bin}" -- ${clippy_checks}
if [ "${autofix}" = "1" ]; then
    cargo fmt
fi
cargo fmt --check

