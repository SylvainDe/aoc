set -x
set -e

# Parse error "available binaries: bin_name1, bin_name2, bin_name3, bin_name4, bin_name5, bin_name6"
for bin in $(cargo run 2>&1 >/dev/null | grep "available binaries" | sed "s/^available binaries://g" | sed "s/,//g");
do
    # Run cargo commands
    cargo run --bin "${bin}"
done

# Run cargo commands
cargo test
cargo clippy -- \
    -D clippy::all \
    -D clippy::correctness \
    -D clippy::suspicious \
    -D clippy::style \
    -D clippy::complexity \
    -D clippy::perf \
    -D clippy::pedantic \
    -D clippy::cargo \
    -D clippy::nursery

