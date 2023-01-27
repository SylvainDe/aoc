set -x
set -e

date_=$(date "+%F_%Hh%Mm%Ss")
before="update_${date_}_before.txt"
after="update_${date_}_before.txt"
(rustc -Vv; cargo clippy --version) > "${before}"
rustup update
cargo update
(rustc -Vv; cargo clippy --version) > "${after}"
diff "${before}" "${after}"
