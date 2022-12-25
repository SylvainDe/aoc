#set -x
set -e

# Previous years
for y in $(seq 2015 2022); do
	for d in $(seq 1 25); do
		echo "$d $y"
		# ./new_day.sh "${d}" "${y}"
	done
done

# Current year
# y="2023"
# for d in $(seq 1 21); do
# 	echo "$d $y"
# 	./new_day.sh "${d}" "${y}"
# done
