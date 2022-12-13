set -x
set -e

# Option to fix things automatically (at your own risk)
autofix="1"
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
-D clippy::nursery"
clippy_fix_checks="-D clippy::restriction -A clippy::implicit_return"

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
    cargo clippy --fix ${fix_options} -- ${clippy_checks} ${clippy_fix_checks}
fi
cargo clippy -- ${clippy_checks}

if [ "${autofix}" = "1" ]; then
    cargo fmt
fi
cargo fmt --check

