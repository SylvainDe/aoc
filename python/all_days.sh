set -e

for year in */;
do
	echo "${year}";
	(cd "${year}" && python3 "all_days.py")
done


