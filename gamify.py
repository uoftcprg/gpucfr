from argparse import ArgumentParser
from pathlib import Path

from tqdm import trange, tqdm
import noregret as nr


def parse_args():
    parser = ArgumentParser()

    parser.add_argument('game')
    parser.add_argument('data', type=Path)

    return parser.parse_args()


def main():
    args = parse_args()
    ker = nr.FPKer()
    game = nr.OpenSpielGame(ker, args.game)
    node_count = 0
    node_hashes = []
    action_counts = {}
    players = {}
    parent_node_hashes = {}
    utilities = {}
    information_set_hashes = {}
    information_set_indices = {}

    def dfs(node, depth, parent_node_hash):
        nonlocal node_count

        node_count += 1
        node_hash = node_count

        while len(node_hashes) <= depth:
            node_hashes.append([])

        node_hashes[depth].append(node_hash)

        children = game.children(node)
        action_counts[node_hash] = len(children)
        i = game.player(node)
        players[node_hash] = 0 if i is None else i + 1
        parent_node_hashes[node_hash] = parent_node_hash
        utilities[node_hash] = game.utility(node, 0)

        if i is None and children:
            raise ValueError('Chance nodes are not supported in Rudolf games')

        if children:
            j = game.information_set(node)

            if j not in information_set_indices:
                information_set_indices[j] = len(information_set_indices)

            information_set_hash = information_set_indices[j] + 1
        else:
            information_set_hash = 0

        information_set_hashes[node_hash] = information_set_hash

        for child in children:
            dfs(child, depth + 1, node_hash)

    dfs(game.root_node, 0, 0)

    with open(args.data, 'w') as file:
        depth_count = len(node_hashes)

        print(depth_count, file=file)

        for depth in trange(depth_count):
            print(len(node_hashes[depth]), file=file)

            for node_hash in tqdm(node_hashes[depth], leave=False):
                print(node_hash, file=file)
                print(action_counts[node_hash], file=file)
                print(players[node_hash], file=file)
                print(parent_node_hashes[node_hash], file=file)
                print(utilities[node_hash], file=file)
                print(information_set_hashes[node_hash], file=file)


if __name__ == '__main__':
    main()
