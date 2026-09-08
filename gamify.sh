set -e

source games.sh

for key in ${!games[@]}; do
	python gamify.py ${games[$key]} data/games/$key.game
	python gamify-test.py data/games/$key.game data/games/$key-test.game
	cmp data/games/$key.game data/games/$key-test.game
	rm data/games/$key-test.game
done
