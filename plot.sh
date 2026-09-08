source games.sh

for key in ${!games[@]}; do
	python plot-exploitabilities.py $key figures/exploitabilities.pdf 'Ours (correct)' data/exploitabilities/$key-noregret.csv 'Rudolf (incorrect)' data/exploitabilities/$key-gpucfr.csv
done
