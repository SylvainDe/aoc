#set -x
set -e

for y in $(seq 2015 2021); do
	for d in $(seq 1 25); do
		echo "$d $y"
		# ./new_day.sh "${d}" "${y}"
	done
done
