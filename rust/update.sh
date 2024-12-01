set -x
set -e

date_=$(date "+%F_%Hh%Mm%Ss")
path="./updates"
before="${path}/update_${date_}_before.txt"
after="${path}/update_${date_}_after.txt"
(rustc -Vv; cargo clippy --version) > "${before}"
rustup update
cargo update
(rustc -Vv; cargo clippy --version) > "${after}"
diff "${before}" "${after}"
