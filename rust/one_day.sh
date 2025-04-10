#set -x
set -e

# Retrieve date
real_day=$(date "+%-d")
real_year=$(date "+%Y")

# Get date used based on user parameters and default to current day
day="${1:-$real_day}"
year="${2:-$real_year}"

# Configure what is triggered
do_check="1"
do_test="1"
do_run="1"
do_clippy="1"
do_fmt="1"

# Option to fix things automatically (at your own risk)
autofix="0"
fix_options="--allow-dirty --allow-staged"

# Bin name
bin="${year}_day${day}"

# Clippy options
clippy_checks="-D clippy::all
-D clippy::correctness
-D clippy::suspicious
-A clippy::blanket_clippy_restriction_lints
-D clippy::style
-D clippy::complexity
-D clippy::perf
-D clippy::pedantic
-D clippy::cargo
-D clippy::nursery
-D clippy::restriction
-A clippy::arbitrary_source_item_ordering
-A clippy::large_stack_arrays
-A clippy::indexing_slicing
-A clippy::iter_over_hash_type
-A clippy::arithmetic_side_effects
-A clippy::modulo_arithmetic
-A clippy::integer_division_remainder_used
-A clippy::default_numeric_fallback
-A clippy::implicit_return
-A clippy::missing_assert_message
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
-A clippy::string_slice
-A clippy::assertions_on_result_states
-A clippy::question_mark_used
-A clippy::std_instead_of_alloc
-A clippy::std_instead_of_core
-A clippy::min_ident_chars
-A clippy::single_call_fn"

# Move to correct directory
cd "$(dirname "$0")"

# Run cargo commands
if [ "${do_check}" = "1" ]; then
    cargo check --lib
    cargo check --bin "${bin}"
fi

if [ "${autofix}" = "1" ]; then
    cargo fix ${fix_options} --lib
    cargo fix ${fix_options} --bin "${bin}"
fi

if [ "${do_test}" = "1" ]; then
    cargo test --lib
    cargo test --bin "${bin}" -- --nocapture --test-threads=1
fi

if [ "${do_run}" = "1" ]; then
    cargo run --bin "${bin}"
fi

if [ "${do_clippy}" = "1" ]; then
    if [ "${autofix}" = "1" ]; then
        cargo clippy --fix ${fix_options} --lib          -- ${clippy_checks}
        cargo clippy --fix ${fix_options} --bin "${bin}" -- ${clippy_checks}
    fi
    cargo clippy --lib          -- ${clippy_checks}
    cargo clippy --bin "${bin}" -- ${clippy_checks}
fi

if [ "${do_fmt}" = "1" ]; then
    if [ "${autofix}" = "1" ]; then
        cargo fmt
    fi
    cargo fmt --check
fi
