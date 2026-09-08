source games.sh
source iterations.sh

for key in ${!games[@]}; do
	for iteration in $iterations; do
		./cmake-build-debug/gpucfr $iteration data/games/$key.game > data/solutions/$key-$iteration.txt
	done
done
