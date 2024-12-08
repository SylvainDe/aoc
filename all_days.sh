#set -x
set -e

aoc_browser=""
aoc_editor=""

# Previous years
first_year=2015
last_full_year=2023
first_day=1
last_day=25
for y in $(seq ${first_year} ${last_full_year}); do
	for d in $(seq ${first_day} ${last_day}); do
		echo "$d $y"
		# ./new_day.sh "${d}" "${y}"
	done
done

# Current year
real_year=$(date "+%Y")
real_month=$(date "+%m")
real_day=$(date "+%-d")
if [[ "${real_year}" -gt "${last_full_year}" ]] && [ "${real_month}" = "12" ]; then
	for d in $(seq ${first_day} ${real_day}); do
		echo "$d ${real_year}"
		#./new_day.sh "${d}" "${real_year}"
	done
fi
