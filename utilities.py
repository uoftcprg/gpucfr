from collections import defaultdict, deque
from dataclasses import dataclass, field
from functools import partial

from ordered_set import OrderedSet
import noregret as nr


@dataclass
class RudolfGame(nr.BlackBoxGame):
    content: str
    _nodes: list[int] = field(init=False, default_factory=list)
    _action_counts: dict[int, int] = field(init=False, default_factory=dict)
    _children: defaultdict[int, list[int]] = field(
        init=False,
        default_factory=partial(defaultdict, list),
    )
    _players: dict[int, int] = field(init=False, default_factory=dict)
    _utilities: dict[int, float] = field(init=False, default_factory=dict)
    _information_sets: dict[int, int] = field(init=False, default_factory=dict)

    def __post_init__(self):
        tokens = deque(self.content.split())
        depth_count = int(tokens.popleft())

        for depth in range(depth_count):
            node_count = int(tokens.popleft())

            for _ in range(node_count):
                h = int(tokens.popleft())
                self._action_counts[h] = int(tokens.popleft())
                self._players[h] = int(tokens.popleft()) - 1
                p_h = int(tokens.popleft())
                self._utilities[h] = float(tokens.popleft())
                self._information_sets[h] = int(tokens.popleft())

                self._nodes.append(h)
                self._children[p_h].append(h)

        if tokens:
            raise ValueError('some tokens remain')

    @property
    def player_count(self):
        return 2

    @property
    def is_zero_sum(self):
        return True

    @property
    def root_node(self):
        return self._nodes[0]

    def actions(self, node):
        return OrderedSet(range(self._action_counts[node]))

    def apply(self, node, action):
        return self._children[node][action]

    def player(self, node):
        return self._players[node]

    def utility(self, node, player):
        u = self._utilities[node]

        return -u if player else u

    def information_set(self, node):
        return self._information_sets[node]

    def chance_probability(self, node, action):
        raise ValueError('Rudolf games do not support chance nodes')
