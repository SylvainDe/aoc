#set -x
set -e

# Option to fix things automatically (at your own risk)
autofix="0"
fix_options="--allow-dirty --allow-staged"

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
    cargo fix ${fix_options}
fi

cargo test

# Parse error "available binaries: bin_name1, bin_name2, bin_name3, bin_name4, bin_name5, bin_name6"
for bin in $(cargo run 2>&1 >/dev/null | grep "available binaries" | sed "s/^available binaries://g" | sed "s/,//g");
do
    # Run cargo commands
    cargo run --bin "${bin}"
done

if [ "${autofix}" = "1" ]; then
    cargo clippy --fix ${fix_options} -- ${clippy_checks}
fi
cargo clippy -- ${clippy_checks}

if [ "${autofix}" = "1" ]; then
    cargo fmt
fi
cargo fmt --check

